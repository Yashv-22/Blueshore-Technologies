from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.contact.models import ContactRequest

class ContactRequestModelTest(TestCase):
    def test_contact_request_creation(self):
        contact = ContactRequest.objects.create(
            name="Alice Smith",
            company="Tech Corp",
            email="alice@techcorp.com",
            phone="1234567890",
            service="Web Development",
            budget="10k-25k",
            message="We need a premium marketing site.",
            source_page="/contact.html"
        )
        self.assertEqual(contact.name, "Alice Smith")
        self.assertEqual(contact.status, "New")
        self.assertEqual(str(contact), "Alice Smith - Tech Corp (Web Development)")

class ContactRequestAPITest(APITestCase):
    def test_submit_contact_form(self):
        url = reverse('api-contact-submit')
        data = {
            'name': 'Bob Jones',
            'company': 'Enterprise Inc',
            'email': 'bob@enterprise.com',
            'phone': '9876543210',
            'service': 'AI / Automation Systems',
            'budget': '25k-50k',
            'message': 'Looking for an AI chatbot system integrated into our website.',
            'source_page': '/index.html'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('id', response.data)
        
        # Verify db entry exists
        db_contact = ContactRequest.objects.get(name='Bob Jones')
        self.assertEqual(db_contact.company, 'Enterprise Inc')
        self.assertEqual(db_contact.source_page, '/index.html')

    def test_submit_contact_form_invalid_email(self):
        url = reverse('api-contact-submit')
        data = {
            'name': 'Bob Jones',
            'company': 'Enterprise Inc',
            'email': 'not-an-email',
            'phone': '9876543210',
            'service': 'AI / Automation Systems',
            'budget': '25k-50k',
            'message': 'Looking for an AI chatbot system.',
            'source_page': '/index.html'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('email', response.data['errors'])
