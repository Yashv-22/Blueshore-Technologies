from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.contact.models import ContactRequest
from apps.crm.models import Client, Project, CRMNote, Lead
from apps.crm.admin import parse_budget_string

User = get_user_model()

class CRMIntegrationTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )

    def test_budget_parsing(self):
        # Under $10K -> 10000
        self.assertEqual(parse_budget_string("Under $10K"), Decimal("10000.00"))
        # $10K–$50K -> 50000 (takes upper bound)
        self.assertEqual(parse_budget_string("$10K–$50K"), Decimal("50000.00"))
        # $50K–$200K -> 200000 (takes upper bound)
        self.assertEqual(parse_budget_string("$50K–$200K"), Decimal("200000.00"))
        # $200K+ -> 200000
        self.assertEqual(parse_budget_string("$200K+"), Decimal("200000.00"))
        # None or empty -> 0
        self.assertEqual(parse_budget_string(""), Decimal("0.00"))
        self.assertEqual(parse_budget_string(None), Decimal("0.00"))
        # Simple number -> 1500
        self.assertEqual(parse_budget_string("$1500"), Decimal("1500.00"))

    def test_lead_conversion_creates_client_and_project(self):
        # 1. Create a lead
        lead = Lead.objects.create(
            name="John Doe",
            company="Doe Enterprises",
            email="john@doe.com",
            phone="1234567890",
            service="AI & Automation",
            budget="$10K–$50K",
            message="Need a custom chatbot.",
            source_page="/contact.html"
        )
        
        # 2. Add an inline CRMNote to the lead
        note = CRMNote.objects.create(
            lead=lead,
            author=self.admin_user,
            content="Spoke to John on phone. He wants it ASAP."
        )

        # 3. Simulate convert action
        # Check if client already exists
        client = Client.objects.filter(email=lead.email).first()
        self.assertIsNone(client)
        
        # Create client
        client = Client.objects.create(
            company_name=lead.company,
            contact_person=lead.name,
            email=lead.email,
            phone=lead.phone,
            notes=f"Converted from Lead. Original Message:\n{lead.message}"
        )
        
        # Create project
        project_title = f"{lead.service} - {lead.company}"
        parsed_budget = parse_budget_string(lead.budget)
        project = Project.objects.create(
            client=client,
            title=project_title,
            status='Planning',
            budget=parsed_budget,
            notes=f"Service: {lead.service}\nBudget range: {lead.budget}"
        )

        # Link lead notes to client
        CRMNote.objects.filter(lead=lead).update(client=client)

        # Verify
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Project.objects.count(), 1)
        self.assertEqual(project.budget, Decimal("50000.00"))
        
        # Verify note is now linked to client
        note.refresh_from_db()
        self.assertEqual(note.client, client)
        self.assertEqual(note.lead, lead)

    def test_client_portal_views(self):
        from django.test import Client as TestClient
        c = TestClient()
        
        # Test anonymous redirect
        response = c.get('/portal/')
        self.assertEqual(response.status_code, 302)
        
        # Force login
        c.force_login(self.admin_user)
        response = c.get('/portal/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Client Cockpit')

