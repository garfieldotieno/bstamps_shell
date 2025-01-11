const CACHE_NAME = 'bot-interface-cache-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/favicon.ico',
    '/manifest.json',
    '/static/js/main.js',
    '/static/css/main.css',
    '/static/js/mds.js',
    '/static/js/data.js',
    '/static/js/philate.js',
];

// Install the service worker and cache assets
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching files');
            return cache.addAll(urlsToCache);
        })
    );
});

// Fetch and serve files from the cache
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

// Activate and clean up old caches
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
