from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.newsletter.models import NewsletterSubscriber
from apps.newsletter.serializers import NewsletterSubscriberSerializer
from apps.core.throttling import NewsletterRateThrottle

class NewsletterSubscribeAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    throttle_classes = [NewsletterRateThrottle]


    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip().lower()
        if not email:
            return Response({
                'success': False,
                'message': 'Email address is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if they already exist
        subscriber = NewsletterSubscriber.objects.filter(email=email).first()
        if subscriber:
            if subscriber.is_active:
                return Response({
                    'success': True,
                    'message': 'You are already subscribed to our newsletter!'
                }, status=status.HTTP_200_OK)
            else:
                subscriber.is_active = True
                subscriber.save()
                return Response({
                    'success': True,
                    'message': 'Welcome back! Your subscription has been reactivated.'
                }, status=status.HTTP_200_OK)

        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Thank you for subscribing to our newsletter!'
            }, status=status.HTTP_201_CREATED)
        
        # Format errors cleanly
        error_msg = list(serializer.errors.values())[0][0] if serializer.errors else "Invalid data."
        return Response({
            'success': False,
            'message': error_msg,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
