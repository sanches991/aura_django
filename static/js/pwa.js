(function () {
  'use strict';

  var bannerId = 'pwaOfflineBanner';

  function ensureStyle() {
    if (document.getElementById('pwaOfflineStyle')) return;
    var style = document.createElement('style');
    style.id = 'pwaOfflineStyle';
    style.textContent = [
      '.pwa-offline-banner{position:fixed;left:50%;bottom:14px;z-index:1000;transform:translate(-50%,18px);opacity:0;pointer-events:none;padding:9px 14px;border-radius:999px;background:#14231a;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.24);font:700 12px system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;letter-spacing:.04em;text-transform:uppercase;transition:opacity .2s ease,transform .2s ease}',
      '.pwa-offline-banner.is-visible{opacity:1;transform:translate(-50%,0)}'
    ].join('');
    document.head.appendChild(style);
  }

  function ensureBanner() {
    ensureStyle();
    var existing = document.getElementById(bannerId);
    if (existing) return existing;

    var banner = document.createElement('div');
    banner.id = bannerId;
    banner.className = 'pwa-offline-banner';
    banner.setAttribute('role', 'status');
    banner.setAttribute('aria-live', 'polite');
    banner.textContent = 'Offline mode';
    document.body.appendChild(banner);
    return banner;
  }

  function updateNetworkState() {
    var banner = ensureBanner();
    banner.classList.toggle('is-visible', !navigator.onLine);
    document.documentElement.classList.toggle('is-offline', !navigator.onLine);
  }

  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/service-worker.js', { scope: '/' }).catch(function () {
        // Registration failure should not affect the menu UX.
      });
    });
  }

  window.addEventListener('online', updateNetworkState);
  window.addEventListener('offline', updateNetworkState);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateNetworkState);
  } else {
    updateNetworkState();
  }
})();
