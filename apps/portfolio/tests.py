from django.test import TestCase
from django.urls import reverse
from apps.portfolio.models import PortfolioProject

class PortfolioModelTest(TestCase):
    def test_project_creation(self):
        project = PortfolioProject.objects.create(
            title="Global Logistics Redesign",
            category="Logistics",
            challenge="Old slow systems.",
            strategy="AWS cloud migrate.",
            solution="Decoupled Kubernetes.",
            results="Fast shipment scaling.",
            metric_1_value="Zero",
            metric_1_label="Downtime",
            metric_2_value="58%",
            metric_2_label="Shorter CAC",
            is_published=True
        )
        self.assertEqual(project.slug, "global-logistics-redesign")
        self.assertEqual(str(project), "Global Logistics Redesign")

class PortfolioViewTest(TestCase):
    def test_portfolio_page_contains_projects(self):
        PortfolioProject.objects.create(
            title="Dynamic Fintech Hub",
            category="Fintech",
            challenge="Unscalable payments.",
            strategy="Decouple ledger.",
            solution="Kafka event cluster.",
            results="10k transaction per second.",
            metric_1_value="10k+",
            metric_1_label="Transactions",
            metric_2_value="99.999%",
            metric_2_label="Uptime",
            is_published=True
        )
        
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dynamic Fintech Hub")
        self.assertContains(response, "Kafka event cluster.")
