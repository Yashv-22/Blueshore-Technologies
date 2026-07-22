import os
import uuid
from django.db import models
from django.utils.text import slugify

def get_resume_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    random_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', random_filename)


class JobListing(models.Model):
    CONTRACT_CHOICES = (
        ('Contract', 'Contract'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
    )
    LOCATION_CHOICES = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Delhi NCR', 'Delhi NCR'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    contract_type = models.CharField(max_length=50, choices=CONTRACT_CHOICES, default='Contract')
    hours_per_week = models.CharField(max_length=100, blank=True)
    hourly_rate_range = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Remote')
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Job Listing"
        verbose_name_plural = "Job Listings"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_job_posting_schema(self):
        """Generates dynamic JobPosting JSON-LD Schema for Google Job Search integration"""
        employment_map = {
            'Full-time': 'FULL_TIME',
            'Part-time': 'PART_TIME',
            'Contract': 'CONTRACTOR'
        }
        return {
            "@context": "https://schema.org",
            "@type": "JobPosting",
            "title": self.title,
            "description": self.description,
            "datePosted": self.created_at.strftime('%Y-%m-%d'),
            "validThrough": "2027-12-31",
            "employmentType": employment_map.get(self.contract_type, "OTHER"),
            "hiringOrganization": {
                "@type": "Organization",
                "name": "Blueshore Technologies",
                "sameAs": "https://www.blueshoretech.com"
            },
            "jobLocation": {
                "@type": "Place",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": self.location if self.location != 'Remote' else "Remote",
                    "addressRegion": "Delhi NCR" if self.location != 'Remote' else "Remote",
                    "addressCountry": "IN"
                }
            }
        }

class JobApplication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(JobListing, on_delete=models.SET_NULL, null=True, blank=True, related_name='applications', help_text="Null indicates general freelance roster application")
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField(max_length=150, help_text="Specialty selected (e.g. Frontend, Backend, UI/UX)")
    experience = models.CharField(max_length=100)
    rate = models.CharField(max_length=100)
    portfolio_url = models.URLField(max_length=500)
    linkedin_url = models.URLField(max_length=500, blank=True)
    resume = models.FileField(upload_to=get_resume_upload_path, blank=True, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-created_at']

    def __str__(self):
        type_str = f"Job: {self.job.title}" if self.job else "Freelance Roster"
        return f"{self.fullname} - {type_str}"
