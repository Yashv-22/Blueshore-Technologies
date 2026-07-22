from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from apps.careers.models import JobListing
from apps.careers.serializers import JobApplicationSerializer
from apps.core.throttling import CareersRateThrottle

def careers_view(request):
    jobs = JobListing.objects.filter(is_open=True)
    return render(request, 'careers.html', {'jobs': jobs})

def submit_portfolio_view(request):
    jobs = JobListing.objects.filter(is_open=True)
    return render(request, 'submit-portfolio.html', {'jobs': jobs})

class JobApplicationCreateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    parser_classes = [MultiPartParser, FormParser]  # Enable file upload handling
    throttle_classes = [CareersRateThrottle]


    def post(self, request, *args, **kwargs):
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()
            return Response({
                'success': True,
                'message': 'Your application has been received successfully. Thank you for joining our roster!',
                'id': application.id
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
