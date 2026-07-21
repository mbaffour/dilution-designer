/* Dilution Designer — service worker.
   Precaches the whole app so it works with no network (bench / cold room / BSL suite).
   Bump CACHE on every release so clients pick the new version up. */
const CACHE = 'dd-v1.0.0';

const CORE = [
  './',
  './index.html',
  './reagent-library.json',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png',
  './favicon-32.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    // cache:'reload' so we never precache a stale copy from the HTTP cache
    await Promise.all(CORE.map(async (u) => {
      try { await c.add(new Request(u, { cache: 'reload' })); } catch (_) { /* optional asset */ }
    }));
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)));
    await self.clients.claim();
  })());
});

// The page tells us to take over once the user accepts an update.
self.addEventListener('message', (e) => {
  if (e.data === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  let url;
  try { url = new URL(req.url); } catch (_) { return; }

  // Cross-origin (e.g. the Google Fonts stylesheet) goes straight to the network.
  // Offline it simply fails and the CSS falls back to the local font stack.
  if (url.origin !== self.location.origin) return;

  // Navigations: network-first so a new deploy is picked up, cache as the offline fallback.
  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const net = await fetch(req);
        const c = await caches.open(CACHE);
        c.put('./index.html', net.clone());
        return net;
      } catch (_) {
        const c = await caches.open(CACHE);
        return (await c.match('./index.html')) || (await c.match('./')) || Response.error();
      }
    })());
    return;
  }

  // Same-origin assets: cache-first (instant offline), refreshed in the background.
  e.respondWith((async () => {
    const c = await caches.open(CACHE);
    const hit = await c.match(req, { ignoreSearch: true });
    if (hit) {
      fetch(req).then((r) => { if (r && r.ok) c.put(req, r.clone()); }).catch(() => {});
      return hit;
    }
    try {
      const net = await fetch(req);
      if (net && net.ok) c.put(req, net.clone());
      return net;
    } catch (_) {
      return Response.error();
    }
  })());
});
