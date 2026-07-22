from rest_framework import serializers
from apps.contact.models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['name', 'company', 'email', 'phone', 'service', 'budget', 'message', 'source_page']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'message': {'required': True},
        }
