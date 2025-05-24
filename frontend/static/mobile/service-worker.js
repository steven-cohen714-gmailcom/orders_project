const CACHE_NAME = "urc-mobile-cache-v1";
const urlsToCache = [
  "/mobile/authorisations",
  "/static/mobile/css/authorisations.css",
  "/static/mobile/js/authorisations_screen/main.js",
  "/static/mobile/manifest.json"
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
