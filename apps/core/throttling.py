from rest_framework.throttling import AnonRateThrottle

class ContactRateThrottle(AnonRateThrottle):
    scope = 'contact'

class CareersRateThrottle(AnonRateThrottle):
    scope = 'careers'

class NewsletterRateThrottle(AnonRateThrottle):
    scope = 'newsletter'

class ChatbotRateThrottle(AnonRateThrottle):
    scope = 'chatbot'
