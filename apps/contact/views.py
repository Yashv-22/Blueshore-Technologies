from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.contact.serializers import ContactRequestSerializer
from apps.core.throttling import ContactRateThrottle

def contact_view(request):
    return render(request, 'contact.html')

class ContactRequestCreateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [ContactRateThrottle]


    def post(self, request, *args, **kwargs):
        serializer = ContactRequestSerializer(data=request.data)
        if serializer.is_valid():
            contact_request = serializer.save()
            
            # Here we could trigger a background task (e.g. email notification to admins)
            # using Celery, or create a CRM note, etc.
            
            return Response({
                'success': True,
                'message': 'Your message has been sent successfully. We will contact you shortly.',
                'id': contact_request.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
