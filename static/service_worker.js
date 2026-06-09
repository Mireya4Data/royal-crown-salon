const CACHE_NAME = 'royal-crown-v2';
const urlsToCache = ['/', '/services/', '/gallery/'];

// Install — cache pages
self.addEventListener('install', event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
    );
});

// Activate — delete all old caches
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(
                keys.filter(key => key !== CACHE_NAME)
                    .map(key => caches.delete(key))
            )
        )
    );
    self.clients.claim();
});

// Fetch — network first, fallback to cache
self.addEventListener('fetch', event => {
    // Never cache POST requests or admin/login/register pages
    if (
        event.request.method !== 'GET' ||
        event.request.url.includes('/login') ||
        event.request.url.includes('/register') ||
        event.request.url.includes('/logout') ||
        event.request.url.includes('/book') ||
        event.request.url.includes('/admin') ||
        event.request.url.includes('/my-bookings') ||
        event.request.url.includes('/cancel')
    ) {
        event.respondWith(fetch(event.request));
        return;
    }

    event.respondWith(
        fetch(event.request)
            .then(response => {
                const clone = response.clone();
                caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
                return response;
            })
            .catch(() => caches.match(event.request))
    );
});