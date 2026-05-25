from django.conf import settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, never_cache
from django.views.generic import TemplateView


class ManifestView(TemplateView):
    template_name = "pwa/manifest.json"
    content_type = "application/manifest+json"

    @method_decorator(cache_control(public=True, max_age=3600))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class OfflineView(TemplateView):
    template_name = "pwa/offline.html"

    @method_decorator(cache_control(public=True, max_age=3600))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@never_cache
def service_worker(request):
    response = render(
        request,
        "pwa/service-worker.js",
        {
            "pwa_cache_version": getattr(settings, "PWA_CACHE_VERSION", "dev"),
        },
        content_type="application/javascript",
    )
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"
    response["Service-Worker-Allowed"] = "/"
    response["X-Content-Type-Options"] = "nosniff"
    return response
