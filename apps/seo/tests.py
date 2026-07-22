from django.test import TestCase
from django.urls import reverse
from apps.seo.programmatic_seo import SERVICES_DATA, LOCATIONS_DATA
from apps.seo.models import ServicePillar

class ProgrammaticSEOTests(TestCase):
    def test_programmatic_landing_page_resolves_successfully(self):
        """Verify that a valid combination of service and location returns 200 OK and valid HTML"""
        # Let's test custom-software-development in delhi
        url = reverse('programmatic-seo-landing', kwargs={
            'service_slug': 'custom-software-development',
            'location_slug': 'delhi'
        })
        response = this_response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Custom Software &amp; Web Development Services in Delhi NCR")
        self.assertContains(response, "What Is This?")
        self.assertContains(response, "Common Questions")

    def test_invalid_service_or_location_returns_404(self):
        """Verify that invalid slugs return 404 Not Found"""
        # Invalid service
        url = reverse('programmatic-seo-landing', kwargs={
            'service_slug': 'non-existent-service',
            'location_slug': 'delhi'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        # Invalid location
        url = reverse('programmatic-seo-landing', kwargs={
            'service_slug': 'custom-software-development',
            'location_slug': 'non-existent-city'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_dynamic_sitemap_includes_programmatic_urls(self):
        """Verify that the sitemap XML includes programmatic routes"""
        url = reverse('dynamic-sitemap')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')
        
        # Check if sitemap contains at least one programmatic URL
        expected_url = "https://www.blueshoretech.com/custom-software-development/delhi/"
        self.assertContains(response, expected_url)

    def test_service_pillar_page_resolves_successfully(self):
        """Verify that a database-seeded service pillar page loads and renders details"""
        # Create a test pillar
        pillar = ServicePillar.objects.create(
            service_slug="test-service-slug",
            name="Test Service Pillar",
            title="Test SEO Title",
            description="Test Description",
            tagline="Test Tagline",
            body_content="<p>Test Main Body Content</p>",
            tech_stack_json=[{"name": "Django", "icon": "django"}],
            case_studies_json=[{"title": "Test Case", "metric": "Test Metric", "desc": "Test Desc"}]
        )
        
        url = reverse('service-pillar', kwargs={'service_slug': 'test-service-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Service Pillar")
        self.assertContains(response, "Test Tagline")
        self.assertContains(response, "Test Main Body Content")
        
    def test_non_existent_service_pillar_returns_404(self):
        """Verify that a non-existent service slug returns 404"""
        url = reverse('service-pillar', kwargs={'service_slug': 'non-existent-slug'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_dynamic_sitemap_includes_service_pillars(self):
        """Verify that the sitemap XML includes dynamic service pillar URLs"""
        # Create a test pillar
        pillar = ServicePillar.objects.create(
            service_slug="sitemap-test-slug",
            name="Sitemap Test Pillar",
            title="Sitemap Test",
            description="Sitemap Test Desc",
            tagline="Sitemap Test Tagline",
            body_content="<p>Sitemap test body</p>",
            tech_stack_json=[]
        )
        
        url = reverse('dynamic-sitemap')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://www.blueshoretech.com/services/sitemap-test-slug/")


