from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Lead(TimeStampedModel):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal'),
        ('negotiation', 'Negotiation'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    next_follow_up = models.DateTimeField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.company}"

    class Meta:
        ordering = ['-created_at']


class Client(TimeStampedModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    lead = models.OneToOneField(
        Lead, on_delete=models.SET_NULL, null=True, related_name='client')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active')
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='assigned_clients')
    next_follow_up = models.DateTimeField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.company}"

    class Meta:
        ordering = ['-created_at']


class Note(TimeStampedModel):
    content = models.TextField()
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='lead_notes')
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True, related_name='client_notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Note by {self.created_by.username} on {self.created_at}"

    class Meta:
        ordering = ['-created_at']


class FollowUp(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='lead_followups')
    client = models.ForeignKey(Client, on_delete=models.CASCADE,
                               null=True, blank=True, related_name='client_followups')
    scheduled_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Follow-up on {self.scheduled_date}"

    class Meta:
        ordering = ['scheduled_date']
