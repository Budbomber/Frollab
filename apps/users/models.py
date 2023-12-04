from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.task_management.models import Task


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=100, blank=True)
    website_url = models.CharField(max_length=100, blank=True)

    def assigned_tasks(self):
        return Task.objects.filter(assignee=self.user)

    def __str__(self):
        return f'{self.user.username.capitalize()}s Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
