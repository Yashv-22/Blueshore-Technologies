from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.intelligence.models import VisitorSession, VisitorTimelineEvent, SessionReplayFrame
from apps.contact.models import ContactRequest
import uuid

class VisitorIntelligenceTestCase(TestCase):
    def setUp(self):
        # Create a test staff user
        self.staff_user = User.objects.create_user(
            username='admin_test',
            email='admin@blueshore.com',
            password='testpassword123',
            is_staff=True
        )
        # Create a normal user
        self.normal_user = User.objects.create_user(
            username='normal_test',
            email='user@blueshore.com',
            password='testpassword123',
            is_staff=False
        )
        
        # Create a test session
        self.session = VisitorSession.objects.create(
            visitor_id='vis_123456',
            session_id='sess_123456',
            ip_address='127.0.0.1',
            browser='Google Chrome',
            device='Desktop',
            os='Windows',
            country='India',
            city='Delhi NCR',
            current_url='http://127.0.0.1:8000/',
            current_page_title='Home',
            is_online=True,
            lead_score=20
        )
        
        # Create a timeline event
        self.timeline_event = VisitorTimelineEvent.objects.create(
            session=self.session,
            event_type='Arrival',
            description='Arrived on Home Page'
        )

    def test_session_creation(self):
        session = VisitorSession.objects.get(session_id='sess_123456')
        self.assertEqual(session.visitor_id, 'vis_123456')
        self.assertEqual(session.lead_score, 20)
        self.assertTrue(session.is_online)

    def test_timeline_event_relation(self):
        event = VisitorTimelineEvent.objects.get(session=self.session, event_type='Arrival')
        self.assertEqual(event.description, 'Arrived on Home Page')

    def test_anonymous_access_denied(self):
        client = Client()
        
        # Test live visitors view
        response = client.get(reverse('live-visitors'))
        self.assertEqual(response.status_code, 302) # Redirect to login
        
        # Test live conversations view
        response = client.get(reverse('live-conversations'))
        self.assertEqual(response.status_code, 302)
        
        # Test visitor analytics view
        response = client.get(reverse('visitor-analytics'))
        self.assertEqual(response.status_code, 302)

    def test_non_staff_access_denied(self):
        client = Client()
        client.force_login(self.normal_user)
        
        response = client.get(reverse('live-visitors'))
        self.assertEqual(response.status_code, 302) # Redirect to login since not staff

    def test_staff_access_granted(self):
        client = Client()
        client.force_login(self.staff_user)
        
        response = client.get(reverse('live-visitors'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Real-Time Visitor Intelligence')
        
        response = client.get(reverse('live-conversations'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active Chats')
        
        response = client.get(reverse('visitor-analytics'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Visitor Engagement Analytics')

    def test_new_views_staff_access(self):
        client = Client()
        client.force_login(self.staff_user)
        
        # Test workspace calendar view
        response = client.get(reverse('workspace-calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workspace Calendar')
        
        # Test SOC Security view
        response = client.get(reverse('security-soc-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Security Operations Center')

    def test_visitor_predictive_properties(self):
        self.assertEqual(self.session.conversion_probability, 24) # 10 base + min(20*0.7, 60) = 24
        self.assertEqual(self.session.urgency, 'Low')
        self.assertEqual(self.session.recommended_service, 'Custom Software Development')

