from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from apps.chatbot.models import ChatConversation, ChatMessage
from apps.contact.models import ContactRequest

class ChatbotModelTest(TestCase):
    def test_conversation_creation(self):
        conv = ChatConversation.objects.create(session_id="session-12345")
        self.assertEqual(conv.session_id, "session-12345")
        self.assertIsNone(conv.lead)
        self.assertEqual(str(conv), "Chat Session: session-12345")

    def test_message_creation(self):
        conv = ChatConversation.objects.create(session_id="session-67890")
        msg = ChatMessage.objects.create(
            conversation=conv,
            sender="User",
            text="Hello, I want to build a website."
        )
        self.assertEqual(msg.conversation, conv)
        self.assertEqual(msg.sender, "User")
        self.assertEqual(msg.text, "Hello, I want to build a website.")
        self.assertEqual(str(msg), "User: Hello, I want to build a website....")

class ChatbotAPITest(APITestCase):
    @patch('apps.chatbot.views.genai.GenerativeModel')
    def test_chat_proxy_endpoint_fallback(self, mock_genai_model):
        from unittest.mock import MagicMock
        mock_chunk = MagicMock()
        mock_chunk.text = "This is a mocked response."
        mock_model_instance = mock_genai_model.return_value
        mock_model_instance.generate_content.return_value = [mock_chunk]

        # We test that the chat proxy endpoint accepts requests, creates session and messages
        url = reverse('api-chatbot-chat')
        data = {
            'session_id': 'test-session-id',
            'contents': [
                {
                    'role': 'user',
                    'parts': [{'text': 'Hello, what services do you offer?'}]
                }
            ]
        }
        
        # Test request without valid Gemini key returns a pattern-matched response or fallback
        response = self.client.post(url, data, format='json')
        # Since it's a streaming SSE endpoint, response content_type should be text/event-stream
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.headers.get('Content-Type'), 'text/event-stream')
        
        # Consume the streaming content so the generator executes and saves the AI response to the DB
        content = b"".join(response.streaming_content)
        self.assertTrue(len(content) > 0)
        
        # Check that conversation was created
        conv_exists = ChatConversation.objects.filter(session_id='test-session-id').exists()
        self.assertTrue(conv_exists)
        
        # Check that message history was populated
        conv = ChatConversation.objects.get(session_id='test-session-id')
        self.assertEqual(conv.messages.count(), 2)  # One user message, one AI response
        self.assertEqual(conv.messages.first().text, 'Hello, what services do you offer?')

    def test_sanitize_lead_jargon(self):
        from apps.chatbot.utils import sanitize_lead_jargon
        self.assertEqual(
            sanitize_lead_jargon("You are a hot lead! Let's book a call."),
            "We are excited to discuss your project! Let's book a call."
        )
        self.assertEqual(
            sanitize_lead_jargon("Our system flagged this as a warm lead."),
            "Our system flagged this as a qualified project."
        )
        self.assertEqual(
            sanitize_lead_jargon("This is classified as a cold lead."),
            "This is classified as a general inquiry."
        )

    def test_fallback_reply_no_internal_tags(self):
        from apps.chatbot.views import generate_fallback_reply
        reply = generate_fallback_reply("what is the budget?")
        self.assertNotIn("(WARM)", reply)
        self.assertNotIn("(HOT)", reply)
        self.assertNotIn("hot lead", reply.lower())

    def test_fallback_reply_sales_and_internal_process(self):
        from apps.chatbot.views import generate_fallback_reply
        
        # Test sales pathway fallback
        sales_reply = generate_fallback_reply("sales")
        self.assertIn("[button:Book a Strategy Call]", sales_reply)
        self.assertIn("[button:Main Menu]", sales_reply)
        
        # Test internal process pathway fallback
        process_reply = generate_fallback_reply("internal process")
        self.assertIn("[button:Development Sprints]", process_reply)
        self.assertIn("[button:Security & Auditing]", process_reply)
        
        # Test main menu fallback contains the new options
        menu_reply = generate_fallback_reply("main menu")
        self.assertIn("[button:Sales]", menu_reply)
        self.assertIn("[button:Internal Process]", menu_reply)
        self.assertIn("[button:Custom Software]", menu_reply)

