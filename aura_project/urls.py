from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from menu import pwa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('manifest.json', pwa.ManifestView.as_view(), name='pwa-manifest'),
    path('service-worker.js', pwa.service_worker, name='pwa-service-worker'),
    path('offline/', pwa.OfflineView.as_view(), name='pwa-offline'),
]

urlpatterns += i18n_patterns(
    path('', include('menu.urls', namespace='menu')),
    prefix_default_language=False,  # русский без префикса /ru/
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
