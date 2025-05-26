from django.db import models
from django.contrib.auth import get_user_model
import os
import uuid
from django.utils.deconstruct import deconstructible
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Event(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("mid",    "Medium"),
        ("low",    "Low"),
    ]

    user      = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title     = models.CharField(max_length=200)
    desc      = models.TextField(blank=True)
    start     = models.DateField()
    time      = models.TimeField(null=True, blank=True)
    end       = models.DateField(null=True, blank=True)
    client    = models.CharField(max_length=200, blank=True)
    priority  = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default="mid")
    created   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start})"
    
class Client(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes about the client")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_full_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'notes': self.notes,
            'created_at': self.created_at
        }
    
@deconstructible
class UniqueFilePath:
    def __init__(self, sub_path="uploads"):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"
        return os.path.join(self.sub_path, filename)

class File(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/', null=True, blank=True) 
    external_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Signal to create/update user profile
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()