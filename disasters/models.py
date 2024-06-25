# disasters/models.py
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class DisasterEvent(models.Model):

    EVENT_TYPE_CHOICES = [
        ('Flood', 'Flood'),
        ('Earthquake', 'Earthquake'),
        ('Tornado', 'Tornado'),
        ('Wildfire', 'Wildfire'),
        ('Hurricane', 'Hurricane'),
        ('Volcano', 'Volcano'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    date_occurred = models.DateTimeField()
    location = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Report(models.Model):
    event = models.ForeignKey(DisasterEvent, on_delete=models.CASCADE)
    reporter_name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    report_date = models.DateTimeField(auto_now_add=True)
    details = models.TextField()

    def __str__(self):
        return f'Report by {self.reporter_name} on {self.event.name}'

class Resource(models.Model):
    event = models.ForeignKey(DisasterEvent, on_delete=models.CASCADE)
    resource_type = models.CharField(max_length=50)
    quantity = models.IntegerField()
    def __str__(self):
        return f'{self.resource_type} for {self.event.name}'
