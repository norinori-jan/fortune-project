/**
 * service-worker.js — タロット鑑定(オフライン版)
 *
 * このアプリは file:// で直接開くことも想定しているため、
 * Service Worker はホストされた場合(https:// または http://localhost)
 * にのみ登録される（app.js側で location.protocol をチェックしている）。
 * file:// では Service Worker 自体が動作しない仕様のため、これは無害。
 */

const CACHE_NAME = "tarot-offline-v1";
const CORE_ASSETS = [
  "./",
  "./index.html",
  "./app.js",
  "./cards_data.js",
  "./manifest.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((key) => key !== CACHE_NAME)
          .map((key) => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// キャッシュ優先、無ければネットワーク（オフラインでも基本機能が動くように）
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) return cached;
      return fetch(event.request).catch(() => cached);
    })
  );
});
