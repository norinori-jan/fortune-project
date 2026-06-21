/**
 * registry-loader.js
 * ================================================================================
 * 
 * Unified Registry Loader for Feng Shui Compass
 * iPhone 17 Pro UI & AR Goggle Ready
 * 
 * Usage:
 *   const loader = RegistryLoader.getInstance();
 *   const registry = await loader.getRegistry();
 *   const mountain = registry.twenty_four_mountains[5];
 * 
 * ================================================================================
 */

class RegistryLoader {
  constructor() {
    this.registry = null;
    this.lastFetch = 0;
    this.cacheTTL = 86400; // 24 hours
    this.registryURL = "https://norinori-jan.github.io/fortune-core/registry_a.json";
    // Fallback URLs for development
    this.fallbackURLs = [
      "./registry_a.json",
      "../registry_a.json",
      "/registry_a.json",
    ];
  }

  static getInstance() {
    if (!RegistryLoader.instance) {
      RegistryLoader.instance = new RegistryLoader();
    }
    return RegistryLoader.instance;
  }

  /**
   * Check if cached registry is still valid
   */
  isCacheValid() {
    if (!this.registry) return false;
    const now = Date.now();
    return now - this.lastFetch < this.cacheTTL * 1000;
  }

  /**
   * Fetch registry from GitHub Pages or local fallback
   */
  async getRegistry(force = false) {
    if (this.isCacheValid() && !force) {
      return this.registry;
    }

    try {
      // Try GitHub Pages first
      console.log(`[RegistryLoader] Fetching from ${this.registryURL}`);
      const response = await fetch(this.registryURL, {
        mode: "cors",
        cache: "default",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      this.registry = await response.json();
      this.lastFetch = Date.now();
      console.log("[RegistryLoader] ✅ Loaded from GitHub Pages");
      return this.registry;
    } catch (error) {
      console.warn(`[RegistryLoader] GitHub Pages fetch failed: ${error.message}`);
      console.log("[RegistryLoader] Trying fallback URLs...");

      // Try fallback URLs
      for (const url of this.fallbackURLs) {
        try {
          console.log(`[RegistryLoader] Trying ${url}`);
          const response = await fetch(url, { cache: "no-cache" });
          if (response.ok) {
            this.registry = await response.json();
            this.lastFetch = Date.now();
            console.log(`[RegistryLoader] ✅ Loaded from ${url}`);
            return this.registry;
          }
        } catch (e) {
          // Continue to next fallback
        }
      }

      throw new Error(
        "Failed to load registry from all sources. Check network or file paths."
      );
    }
  }

  /**
   * Get mountain info by degree
   * @param {number} degree - Compass bearing 0-360
   * @returns {Object} Mountain data or null
   */
  async getMountainByDegree(degree) {
    const registry = await this.getRegistry();
    const normalized = degree % 360;

    for (const mountain of registry.twenty_four_mountains) {
      const { start_deg, end_deg } = mountain;

      // Handle wrap-around case (e.g., north 0°)
      if (start_deg > end_deg) {
        if (normalized >= start_deg || normalized < end_deg) {
          return mountain;
        }
      } else {
        if (normalized >= start_deg && normalized < end_deg) {
          return mountain;
        }
      }
    }

    return null; // Should not happen with valid registry
  }

  /**
   * Get bagua info by name
   * @param {string} name - Bagua name (e.g., "乾", "兌", etc.)
   * @returns {Object} Bagua data
   */
  async getBaguaByName(name) {
    const registry = await this.getRegistry();
    const bagua = registry.bagua.find((b) => b.id === name);
    if (!bagua) {
      throw new Error(`Unknown bagua: ${name}`);
    }
    return bagua;
  }

  /**
   * Get five element info
   * @param {string} element - Element name (木, 火, 土, 金, 水)
   * @returns {Object} Element data
   */
  async getFiveElementInfo(element) {
    const registry = await this.getRegistry();
    const elem = registry.five_elements[element];
    if (!elem) {
      throw new Error(`Unknown element: ${element}`);
    }
    return elem;
  }

  /**
   * Get direction profile
   * @param {string} direction - Direction key (north, south, east, west, etc.)
   * @returns {Object} Direction profile
   */
  async getDirectionProfile(direction) {
    const registry = await this.getRegistry();
    const profile = registry.directional_roles[direction];
    if (!profile) {
      throw new Error(`Unknown direction: ${direction}`);
    }
    return profile;
  }

  /**
   * Get lopan layer info
   * @param {string} layerId - Layer ID (L1, L2, ..., L13)
   * @returns {Object} Layer data
   */
  async getLopanLayer(layerId) {
    const registry = await this.getRegistry();
    const layer = registry.lopan_layers[layerId];
    if (!layer) {
      throw new Error(`Unknown layer: ${layerId}`);
    }
    return layer;
  }

  /**
   * Generate AR-compatible quaternion for direction
   * @param {number} degreeOffset - Offset in degrees
   * @returns {Array} [x, y, z, w] quaternion for Three.js
   */
  getDirectionQuaternion(degreeOffset) {
    const rad = (degreeOffset * Math.PI) / 180;
    // Rotation around Y-axis (compass bearing)
    return [
      0, // x
      Math.sin(rad / 2), // y
      0, // z
      Math.cos(rad / 2), // w
    ];
  }

  /**
   * Get all 24 mountains
   */
  async getTwentyFourMountains() {
    const registry = await this.getRegistry();
    return registry.twenty_four_mountains;
  }

  /**
   * Get all bagua
   */
  async getAllBagua() {
    const registry = await this.getRegistry();
    return registry.bagua;
  }

  /**
   * Clear cache and force refresh
   */
  clearCache() {
    this.registry = null;
    this.lastFetch = 0;
    console.log("[RegistryLoader] Cache cleared");
  }

  /**
   * Get registry metadata
   */
  async getMeta() {
    const registry = await this.getRegistry();
    return registry.meta;
  }

  /**
   * Debug: Print current cache status
   */
  getStatus() {
    return {
      cached: !!this.registry,
      age_ms: this.registry ? Date.now() - this.lastFetch : null,
      ttl_ms: this.cacheTTL * 1000,
      url: this.registryURL,
    };
  }
}

// Export for use in modules
if (typeof module !== "undefined" && module.exports) {
  module.exports = RegistryLoader;
}

// Example usage (uncomment to test)
/*
(async () => {
  try {
    const loader = RegistryLoader.getInstance();
    const registry = await loader.getRegistry();
    console.log("Registry loaded:", registry.meta);

    // Test: Get mountain at 45 degrees
    const mountain = await loader.getMountainByDegree(45);
    console.log("Mountain at 45°:", mountain);

    // Test: Get bagua
    const bagua = await loader.getBaguaByName("乾");
    console.log("Bagua 乾:", bagua);

    // Test: Quaternion
    const quat = loader.getDirectionQuaternion(90);
    console.log("Quaternion for 90°:", quat);

    console.log("Loader status:", loader.getStatus());
  } catch (error) {
    console.error("Error:", error.message);
  }
})();
*/
