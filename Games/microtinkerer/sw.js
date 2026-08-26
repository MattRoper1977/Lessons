/* Micro-Tinkerer: The Giant's Study — offline cache.
 *
 * The game is one HTML file, so the "app shell" is that file and nothing else.
 * Cache-first: once installed, a load never waits on the network.
 *
 * skipWaiting() is deliberately absent. A new build takes over the next time
 * the game is fully closed, never by swapping the page out from under someone
 * who is four minutes into a hunt.
 *
 * Off-origin requests are passed straight through and never cached: the
 * signalling WebSocket and any relay traffic must not touch this.
 */
const CACHE = 'micro-tinkerer-1.2.0';
const SHELL = ['./', './index.html', './manifest.webmanifest'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(SHELL)));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(request, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(request)
        .then((response) => {
          if (response && response.ok && response.type === 'basic') {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(request, copy));
          }
          return response;
        })
        .catch(() => {
          // Offline and not yet cached. A navigation still gets the game.
          if (request.mode === 'navigate') return caches.match('./index.html');
          return Response.error();
        });
    })
  );
});
