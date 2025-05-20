from django.db import models
from django.contrib.auth import get_user_model
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
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name