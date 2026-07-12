const CACHE_NAME = 'havg-cache-v1';
const ASSETS_TO_CACHE = [
    '/',
    '/assets/style.css',
    '/assets/search.js',
    '/assets/icon-192.png',
    '/assets/icon-512.png',
    '/assets/author.png'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
        .then((cache) => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Stale-while-revalidate strategy for assets, Network-first for HTML pages
    if (event.request.destination === 'document') {
        event.respondWith(
            fetch(event.request).catch(() => caches.match(event.request))
        );
    } else {
        event.respondWith(
            caches.match(event.request).then((cachedResponse) => {
                const networkFetch = fetch(event.request).then((response) => {
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, response.clone());
                    });
                    return response;
                }).catch(() => {
                    // Fallback
                });
                return cachedResponse || networkFetch;
            })
        );
    }
});
