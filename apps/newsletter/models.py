import uuid
from django.db import models

class NewsletterSubscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email


class DripCampaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Drip Campaign"
        verbose_name_plural = "Drip Campaigns"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class CampaignStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    campaign = models.ForeignKey(DripCampaign, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField(default=1)
    delay_days = models.IntegerField(default=1, help_text="Number of days to wait before sending this step.")
    subject = models.CharField(max_length=255)
    body = models.TextField(help_text="Email body text/HTML.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Campaign Step"
        verbose_name_plural = "Campaign Steps"
        ordering = ['step_number']

    def __str__(self):
        return f"Step {self.step_number}: {self.subject} ({self.campaign.name})"

