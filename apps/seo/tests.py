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

    def test_parent_service_hub_resolves_without_404(self):
        """Verify that parent service folders return 200 or 301 redirect instead of 404"""
        url = reverse('parent-service-hub', kwargs={'service_slug': 'crm-integrations'})
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 301, 302])

        url2 = reverse('parent-service-hub', kwargs={'service_slug': 'custom-software-development'})
        response2 = self.client.get(url2)
        self.assertIn(response2.status_code, [200, 301, 302])

    def test_homepage_stat_numbers_pre_rendered(self):
        """Verify that raw HTML DOM contains pre-rendered metric values for crawlers"""
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "15+")
        self.assertContains(response, "500+")
        self.assertContains(response, "98%")
        self.assertContains(response, "40+")

    def test_author_list_view_resolves_successfully(self):
        """Verify that /authors/ hub returns 200 OK and valid BreadcrumbList schema"""
        url = reverse('author-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Leadership &amp; Technical Authors")
        self.assertContains(response, "BreadcrumbList")

    def test_conditional_schema_generation(self):
        """Verify conditional JSON-LD schema allocation per route"""
        from apps.seo.schema_engine import generate_page_schemas
        
        # Homepage schema
        home_html = generate_page_schemas(route="/")
        self.assertIn('"@type": "Organization"', home_html)
        self.assertIn('"@type": "WebSite"', home_html)
        
        # Contact page schema
        contact_html = generate_page_schemas(route="/contact.html")
        self.assertIn('"LocalBusiness"', contact_html)
        self.assertIn('"ContactPage"', contact_html)
        
        # Service page schema
        service_html = generate_page_schemas(route="/custom-software-development/")
        self.assertIn('"Service"', service_html)
        self.assertIn('"ProfessionalService"', service_html)

    def test_portfolio_detail_case_study(self):
        """Verify case study detail page loads with CreativeWork / Article schema"""
        from apps.portfolio.models import PortfolioProject
        project = PortfolioProject.objects.create(
            title="Test Case Study",
            slug="test-case-study",
            category="Fintech",
            challenge="Test challenge",
            strategy="Test strategy",
            solution="Test solution",
            results="Test results",
            metric_1_value="312%",
            metric_1_label="Traffic Increase",
            metric_2_value="45%",
            metric_2_label="CAC Reduction",
            is_published=True
        )
        url = reverse('portfolio-detail', kwargs={'slug': 'test-case-study'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Case Study")
        self.assertContains(response, "CreativeWork")
        self.assertContains(response, "312%")

    def test_llms_txt_endpoint(self):
        """Verify that /llms.txt returns 200 OK plain text markdown for AI bots"""
        url = reverse('llms-txt')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/plain", response['Content-Type'])
        self.assertContains(response, "Blueshore Technologies")
        self.assertContains(response, "Core Service Pillars")

    def test_content_quality_scoring_engine(self):
        """Verify quantitative quality scoring calculation and dynamic robots output"""
        from apps.seo.programmatic_seo import calculate_content_quality_score
        service_sample = {
            "intro_template": "Deep unique service content template description for enterprise B2B apps.",
            "capabilities": [{"title": "C1"}, {"title": "C2"}, {"title": "C3"}]
        }
        location_sample = {
            "challenge": "securing financial ledgers and deploying high-availability services"
        }
        faqs_sample = [{"q": "q1", "a": "a1"}, {"q": "q2", "a": "a2"}]
        
        audit = calculate_content_quality_score(service_sample, location_sample, faqs_sample)
        self.assertGreaterEqual(audit["score"], 60)
        self.assertEqual(audit["robots"], "index, follow")
        self.assertTrue(audit["is_indexable"])





