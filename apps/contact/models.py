import uuid
from django.db import models

class ContactRequest(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Contacted', 'Contacted'),
        ('Qualified', 'Qualified'),
        ('Proposal Sent', 'Proposal Sent'),
        ('Won', 'Won'),
        ('Lost', 'Lost'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, default='')
    service = models.CharField(max_length=150, blank=True, default='')
    budget = models.CharField(max_length=100, blank=True, default='')
    message = models.TextField(blank=True, default='')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='New')
    source_page = models.CharField(max_length=255, default='/contact')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contact Request"
        verbose_name_plural = "Contact Requests"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.company} ({self.service})"

