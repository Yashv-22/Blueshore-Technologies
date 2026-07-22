from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.newsletter.models import NewsletterSubscriber

class NewsletterModelTest(TestCase):
    def test_subscriber_creation(self):
        sub = NewsletterSubscriber.objects.create(email="sub@example.com")
        self.assertEqual(sub.email, "sub@example.com")
        self.assertTrue(sub.is_active)
        self.assertEqual(str(sub), "sub@example.com")

    def test_campaign_creation(self):
        from apps.newsletter.models import DripCampaign, CampaignStep
        campaign = DripCampaign.objects.create(name="Onboarding")
        self.assertEqual(campaign.name, "Onboarding")
        
        step = CampaignStep.objects.create(campaign=campaign, step_number=1, subject="Welcome", body="Hi there!")
        self.assertEqual(step.subject, "Welcome")
        self.assertEqual(step.campaign, campaign)


class NewsletterAPITest(APITestCase):
    def test_subscribe_success(self):
        url = reverse('api-newsletter-subscribe')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        
        # Verify db entry
        sub = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertTrue(sub.is_active)

    def test_subscribe_duplicate_email(self):
        NewsletterSubscriber.objects.create(email='test@example.com')
        url = reverse('api-newsletter-subscribe')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'You are already subscribed to our newsletter!')

    def test_subscribe_reactivate_email(self):
        NewsletterSubscriber.objects.create(email='test@example.com', is_active=False)
        url = reverse('api-newsletter-subscribe')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['message'], 'Welcome back! Your subscription has been reactivated.')
        
        # Verify db status
        sub = NewsletterSubscriber.objects.get(email='test@example.com')
        self.assertTrue(sub.is_active)

    def test_subscribe_invalid_email(self):
        url = reverse('api-newsletter-subscribe')
        data = {'email': 'not-an-email'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

