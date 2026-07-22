from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from apps.careers.models import JobListing, JobApplication

class CareersModelTest(TestCase):
    def test_job_listing_creation(self):
        job = JobListing.objects.create(
            title="Senior React Developer",
            description="Build cool UI frontend.",
            contract_type="Contract",
            hours_per_week="20-30",
            hourly_rate_range="$50-$80/hr",
            location="Remote"
        )
        self.assertEqual(job.slug, "senior-react-developer")
        self.assertTrue(job.is_open)
        self.assertEqual(str(job), "Senior React Developer")

    def test_job_application_creation(self):
        job = JobListing.objects.create(
            title="Senior Python Architect",
            description="Build Django code."
        )
        app = JobApplication.objects.create(
            job=job,
            fullname="Jane Doe",
            email="jane@doe.com",
            role="Backend Python/FastAPI Architect",
            experience="5 to 8 years",
            rate="$70 - $90 / hr",
            portfolio_url="https://janedoe.com",
            note="I love Django."
        )
        self.assertEqual(app.job, job)
        self.assertEqual(str(app), "Jane Doe - Job: Senior Python Architect")

class JobApplicationAPITest(APITestCase):
    def setUp(self):
        self.job = JobListing.objects.create(
            title="UI/UX Designer",
            description="Design Figma systems."
        )
        self.url = reverse('api-careers-apply')

    def test_apply_for_job_success(self):
        resume = SimpleUploadedFile("my_resume.pdf", b"%PDF-1.4 mock_pdf_content", content_type="application/pdf")
        data = {
            'job': self.job.id,
            'fullname': 'Charlie Brown',
            'email': 'charlie@brown.com',
            'role': 'UI/UX Product Designer',
            'experience': '3 to 5 years',
            'rate': '$45 - $60 / hr',
            'portfolio_url': 'https://charlie.design',
            'linkedin_url': 'https://linkedin.com/in/charlie',
            'note': 'Available immediately.',
            'resume': resume
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        
        # Verify db entry
        app = JobApplication.objects.get(fullname='Charlie Brown')
        self.assertEqual(app.job, self.job)
        self.assertTrue(app.resume.name.endswith('.pdf'))

    def test_apply_for_job_invalid_extension(self):
        resume = SimpleUploadedFile("malicious_script.sh", b"echo 'bad'", content_type="text/plain")
        data = {
            'job': self.job.id,
            'fullname': 'Charlie Brown',
            'email': 'charlie@brown.com',
            'role': 'UI/UX Product Designer',
            'experience': '3 to 5 years',
            'rate': '$45 - $60 / hr',
            'portfolio_url': 'https://charlie.design',
            'note': 'Available immediately.',
            'resume': resume
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('resume', response.data['errors'])

    def test_apply_for_job_exceeds_size(self):
        # Create an in-memory file larger than 10MB with valid DOCX signature
        large_content = b"PK\x03\x04" + b"0" * (11 * 1024 * 1024)  # 11MB
        resume = SimpleUploadedFile("too_large.docx", large_content, content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        data = {
            'job': self.job.id,
            'fullname': 'Charlie Brown',
            'email': 'charlie@brown.com',
            'role': 'UI/UX Product Designer',
            'experience': '3 to 5 years',
            'rate': '$45 - $60 / hr',
            'portfolio_url': 'https://charlie.design',
            'note': 'Available immediately.',
            'resume': resume
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('resume', response.data['errors'])
