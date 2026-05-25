{% load static %}'use strict';

const CACHE_VERSION = '{{ pwa_cache_version|escapejs }}';
const STATIC_CACHE = `aura-static-${CACHE_VERSION}`;
const PAGE_CACHE = `aura-pages-${CACHE_VERSION}`;
const IMAGE_CACHE = `aura-images-${CACHE_VERSION}`;
const OFFLINE_URL = '/offline/';
const IMAGE_CACHE_LIMIT = 80;

const PRECACHE_URLS = [
  OFFLINE_URL,
  '/',
  '/menu/',
  '/en/',
  '/en/menu/',
  '/ky/',
  '/ky/menu/',
  '{% static "css/style.css" %}',
  '{% static "js/script.js" %}',
  '{% static "js/pwa.js" %}',
  '{% static "images/icon.svg" %}',
  '{% static "images/icon-black.svg" %}',
  '{% static "images/pwa/icon-192.png" %}',
  '{% static "images/pwa/icon-512.png" %}',
  '{% static "images/pwa/icon-maskable-192.png" %}',
  '{% static "images/pwa/icon-maskable-512.png" %}'
];

const SAFE_METHOD = 'GET';
const SAME_ORIGIN = self.location.origin;

function isSameOrigin(url) {
  return url.origin === SAME_ORIGIN;
}

function hasSensitivePath(url) {
  return (
    url.pathname.startsWith('/admin/') ||
    url.pathname.startsWith('/i18n/') ||
    url.pathname === '/service-worker.js' ||
    url.pathname === '/manifest.json'
  );
}

function hasAuthOrCsrfCookie(request) {
  const cookie = request.headers.get('cookie') || '';
  return /(?:^|;\s*)(sessionid|csrftoken)=/.test(cookie);
}

function isCacheableResponse(response) {
  return response && response.ok && response.type === 'basic';
}

async function trimCache(cacheName, limit) {
  const cache = await caches.open(cacheName);
  const keys = await cache.keys();
  if (keys.length <= limit) return;
  await Promise.all(keys.slice(0, keys.length - limit).map((key) => cache.delete(key)));
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => Promise.all(
        PRECACHE_URLS.map((url) => cache.add(new Request(url, { cache: 'reload' })).catch(() => null))
      ))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  const expected = new Set([STATIC_CACHE, PAGE_CACHE, IMAGE_CACHE]);
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((key) => expected.has(key) ? null : caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

async function cacheFirst(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (isCacheableResponse(response)) {
    await cache.put(request, response.clone());
  }
  return response;
}

async function staleWhileRevalidate(request, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(request);
  const network = fetch(request)
    .then(async (response) => {
      if (isCacheableResponse(response)) {
        await cache.put(request, response.clone());
        if (cacheName === IMAGE_CACHE) await trimCache(IMAGE_CACHE, IMAGE_CACHE_LIMIT);
      }
      return response;
    })
    .catch(() => null);

  return cached || network || Response.error();
}

async function networkFirstPage(request) {
  const cache = await caches.open(PAGE_CACHE);
  try {
    const response = await fetch(request);
    const contentType = response.headers.get('content-type') || '';
    if (isCacheableResponse(response) && contentType.includes('text/html')) {
      await cache.put(request, response.clone());
    }
    return response;
  } catch (_error) {
    return (await cache.match(request)) || (await caches.match(OFFLINE_URL));
  }
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== SAFE_METHOD) return;

  const url = new URL(request.url);
  if (!isSameOrigin(url) || hasSensitivePath(url)) return;
  if (hasAuthOrCsrfCookie(request) && request.mode === 'navigate') return;

  if (request.mode === 'navigate') {
    event.respondWith(networkFirstPage(request));
    return;
  }

  if (url.pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  if (url.pathname.startsWith('/media/')) {
    event.respondWith(staleWhileRevalidate(request, IMAGE_CACHE));
  }
});
