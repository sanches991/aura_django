# AURA production PWA audit

Date: 2026-05-25

## Current production findings

- `https://auracafe.kg/menu/` responds with `200`.
- `https://auracafe.kg/manifest.json` responds with `404` before this deploy.
- `https://auracafe.kg/service-worker.js` responds with `404` before this deploy.
- The repository uses `CompressedManifestStaticFilesStorage`, which is correct for hashed static assets and long-lived cache headers.
- `docker-compose.yml` mounted `./staticfiles:/app/staticfiles`, while `Dockerfile` ran `collectstatic` during image build. That bind mount can hide build-time static files with an empty host directory. The startup command now runs `collectstatic` into the mounted directory before Gunicorn starts.
- Largest local media files are 5-9 MB JPGs in `media/dishes/`. This is the largest LCP, bandwidth, and offline quota risk.

## Implemented changes

- Added root PWA endpoints:
  - `/manifest.json`
  - `/service-worker.js`
  - `/offline/`
- Added install metadata to `templates/menu/index.html` and `templates/menu/info.html`.
- Added `static/js/pwa.js` for service worker registration and network state UI.
- Added PNG PWA icons:
  - `static/images/pwa/icon-192.png`
  - `static/images/pwa/icon-512.png`
  - `static/images/pwa/icon-maskable-192.png`
  - `static/images/pwa/icon-maskable-512.png`
  - `static/images/pwa/apple-touch-icon.png`
- Added service worker cache version setting:
  - `PWA_CACHE_VERSION=2026.05.25.1`
- Added nginx locations for service worker and manifest so they are not treated as immutable static files.

## Service worker strategy

- Static assets: cache-first.
- Menu/info pages: network-first with cached fallback and `/offline/` fallback.
- Media images: stale-while-revalidate with an image cache limit.
- Cache invalidation: versioned cache names derived from `PWA_CACHE_VERSION`.
- Cache cleanup: old static/page/image caches are deleted during `activate`.
- Safety rules:
  - Does not cache non-GET requests.
  - Does not intercept cross-origin requests.
  - Does not cache `/admin/`, `/i18n/`, `/service-worker.js`, or `/manifest.json`.
  - Avoids caching navigations with `sessionid` or `csrftoken` cookies.

## Static files strategy

- Keep `STATIC_URL=/static/`.
- Keep `STATIC_ROOT=/app/staticfiles` in container.
- Keep `CompressedManifestStaticFilesStorage` for hashed filenames and gzip/brotli artifacts.
- nginx can keep `Cache-Control: public, immutable` for `/static/`.
- Service worker and manifest are Django views at root paths, not static files.
- Deploy must run `collectstatic` after code update. The compose command now does this automatically.

## nginx requirements

Use the updated `nginx/menu.barca.kg.conf` locations:

- `location = /service-worker.js`
  - proxies to Django
  - `Cache-Control: no-cache, no-store, must-revalidate`
  - `Service-Worker-Allowed: /`
- `location = /manifest.json`
  - proxies to Django
  - `Cache-Control: public, max-age=3600`
- `/static/`
  - aliases collected static files
  - `Cache-Control: public, immutable`
- `/media/`
  - aliases uploaded media
  - `Cache-Control: public`

Run before reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Safe deployment

1. Back up current release and database.
2. Deploy code to staging or a separate production candidate directory.
3. Build and start containers:

```bash
docker-compose build aura-web
docker-compose up -d aura-web
```

4. Verify inside the container:

```bash
docker exec aura-web python manage.py check --deploy
docker exec aura-web python manage.py collectstatic --noinput --dry-run
```

5. Verify host static directory is populated:

```bash
ls -lah /srv/aura/staticfiles
```

6. Reload nginx after applying config:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

7. Verify:

```bash
curl -I https://auracafe.kg/menu/
curl -I https://auracafe.kg/manifest.json
curl -I https://auracafe.kg/service-worker.js
curl -I https://auracafe.kg/static/js/pwa.js
```

Expected:

- `/manifest.json`: `200`, `application/manifest+json`
- `/service-worker.js`: `200`, `application/javascript`, `Service-Worker-Allowed: /`, no-cache headers
- `/static/...`: long-lived immutable cache headers

## Rollback

1. Revert the code release or switch symlink/image tag to the previous release.
2. Bump or remove `PWA_CACHE_VERSION` if you need installed clients to abandon the new cache.
3. Reload nginx after reverting config:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

4. Optional emergency service worker unregister path:
   serve a temporary `/service-worker.js` with:

```javascript
self.addEventListener('install', function (event) { self.skipWaiting(); });
self.addEventListener('activate', function (event) {
  event.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.map(function (key) { return caches.delete(key); }));
  }).then(function () { return self.registration.unregister(); }));
});
```

## Remaining performance work

Priority 1:

- Generate responsive derivatives for dish images, for example 480w/768w WebP and AVIF.
- Render `srcset`/`sizes` in templates.
- Keep original uploads out of card grids.

Implemented baseline:

```bash
docker exec aura-web python manage.py optimize_menu_images --widths 480,768,1200 --quality 82
```

The menu template uses WebP `srcset` only when generated derivatives exist. Without derivatives it falls back to existing uploaded images.

Priority 2:

- Move `info.html` inline CSS into a static file so it is hashed and cached.
- Move `index.html` inline CSS and language dropdown JS into static files.
- Self-host fonts or replace Google Fonts with system fonts for offline-first behavior.

Priority 3:

- Add template fragment caching for public menu pages if menu updates are not minute-by-minute.
- Add database indexes if admin/menu growth makes ordering/filtering slow.
- Add Lighthouse CI in staging and check mobile Performance, PWA, Best Practices, Accessibility, and SEO before release.

## Security considerations

- Keep `ALLOWED_HOSTS` explicit in production. Avoid `*`.
- Keep `CSRF_TRUSTED_ORIGINS` explicit. Avoid `*`.
- Keep `SECURE_PROXY_SSL_HEADER` aligned with nginx `X-Forwarded-Proto`.
- Service worker intentionally avoids admin, POST, CSRF-sensitive, and authenticated navigations.
- SVG snippets stored in database are rendered with `safe`; only trusted admins should be able to edit them.
