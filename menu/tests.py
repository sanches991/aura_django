from django.test import SimpleTestCase
from django.urls import reverse


class PwaEndpointTests(SimpleTestCase):
    def test_manifest_endpoint(self):
        response = self.client.get(reverse("pwa-manifest"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/manifest+json")
        self.assertContains(response, '"display": "standalone"')
        self.assertContains(response, "icon-maskable-512.png")

    def test_service_worker_endpoint(self):
        response = self.client.get(reverse("pwa-service-worker"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertEqual(response["Service-Worker-Allowed"], "/")
        self.assertIn("no-cache", response["Cache-Control"])
        self.assertContains(response, "hasSensitivePath")
        self.assertContains(response, "/admin/")
        self.assertContains(response, "request.method !== SAFE_METHOD")

    def test_offline_endpoint(self):
        response = self.client.get(reverse("pwa-offline"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/menu/"')
