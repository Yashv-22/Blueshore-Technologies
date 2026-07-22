from rest_framework import serializers
from apps.newsletter.models import NewsletterSubscriber

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

    def validate_email(self, value):
        # Check if email exists
        subscriber = NewsletterSubscriber.objects.filter(email__iexact=value).first()
        if subscriber:
            if subscriber.is_active:
                raise serializers.ValidationError("This email is already subscribed to our newsletter.")
            else:
                # If they were unsubscribed, we will re-activate them in the view, so let's allow validation to pass.
                pass
        return value.lower()
