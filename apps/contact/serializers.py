from rest_framework import serializers
from apps.contact.models import ContactRequest

class ContactRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactRequest
        fields = ['name', 'company', 'email', 'phone', 'service', 'budget', 'message', 'source_page']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'message': {'required': False, 'allow_blank': True, 'default': ''},
            'company': {'required': False, 'allow_blank': True, 'default': ''},
            'phone': {'required': False, 'allow_blank': True, 'default': ''},
            'service': {'required': False, 'allow_blank': True, 'default': ''},
            'budget': {'required': False, 'allow_blank': True, 'default': ''},
            'source_page': {'required': False, 'allow_blank': True, 'default': '/contact'},
        }

