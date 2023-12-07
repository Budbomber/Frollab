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
    """

    Create User Profile

    This method is triggered by the post_save signal when a new User instance is created.
     It is responsible for creating a UserProfile instance associated with the newly created User.

    Parameters:
    - sender: The model class which is sending the signal (User in this case)
    - instance: The actual instance of the sending model (the created User instance)
    - created: A boolean indicating whether the instance was created or updated
    - kwargs: Additional keyword arguments

    Return Type:
    None

    Example Usage:
    create_user_profile(sender=User, instance=user, created=True)

    """
    if created:
        UserProfile.objects.create(user=instance)
