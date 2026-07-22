import uuid
from django.db import models
from apps.contact.models import ContactRequest

class ChatConversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_id = models.CharField(max_length=255, unique=True)
    lead = models.ForeignKey(ContactRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat Conversation"
        verbose_name_plural = "Chat Conversations"
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat Session: {self.session_id}"

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('User', 'User'),
        ('AI', 'AI'),
        ('Admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Chat Message"
        verbose_name_plural = "Chat Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

class ChatbotLead(ContactRequest):
    class Meta:
        proxy = True
        verbose_name = "Chatbot Lead"
        verbose_name_plural = "Chatbot Leads"
