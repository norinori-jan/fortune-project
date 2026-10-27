from __future__ import annotations
from fortune_core.models.runtime_health import FortuneRuntimeHealth
from fortune_core.services.runtime_capabilities import (
    FortuneRuntimeCapabilityService,
)
from fortune_core.services.runtime_metrics import (
    FortuneRuntimeMetricsService,
)
from fortune_core.services.service_manifest import (
    FortuneServiceManifestService,
)
class FortuneRuntimeHealthService:
    def __init__(
        self,
        metrics: FortuneRuntimeMetricsService | None = None,
        manifests: FortuneServiceManifestService | None = None,
        capabilities: FortuneRuntimeCapabilityService | None = None,
    ) -> None:
        self.metrics = metrics or FortuneRuntimeMetricsService()
        self.manifests = manifests or FortuneServiceManifestService()
        self.capabilities = (
            capabilities
            or FortuneRuntimeCapabilityService()
        )
    def health(self) -> FortuneRuntimeHealth:
        manifests_ok = len(self.manifests.list()) > 0
        capabilities_ok = len(self.capabilities.list()) > 0
        checks = {
            "manifests": manifests_ok,
            "capabilities": capabilities_ok,
            "metrics": self.metrics is not None,
        }
        healthy = all(checks.values())
        return FortuneRuntimeHealth(
            status="healthy" if healthy else "degraded",
            service="fortune-runtime",
            version="1.0.0",
            checks=checks,
            metrics=self.metrics.snapshot().to_dict(),
        )