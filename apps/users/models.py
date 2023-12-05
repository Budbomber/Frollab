from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.task_management.models import Task


class UserProfile(models.Model):
    """
    Class: UserProfile

    This class represents the user profile of a Django User model. It extends the Django `models.Model` class and
     provides additional fields to store information about the user's organization, job title, profile picture,
     bio, location, contact number, and website URL.

    Attributes:
    - user (OneToOneField): The user associated with this user profile.
    - organization (CharField): The organization the user belongs to. It is a string with a maximum length
    of 100 characters. It can be blank.
    - job_title (CharField): The job title of the user. It is a string with a maximum length of 100 characters.
     It can be blank.
    - profile_picture (ImageField): The profile picture of the user. It is an image file that can be uploaded to the
    'profile_pictures/' directory. It can be blank and nullable.
    - bio (TextField): The biography or description of the user. It is a text field that can be blank.
    - location (CharField): The location of the user. It is a string with a maximum length of 100 characters.
     It can be blank.
    - contact_number (CharField): The contact number of the user. It is a string with a maximum length of 100
     characters. It can be blank.
    - website_url (CharField): The URL of the user's website. It is a string with a maximum length of 100
     characters. It can be blank.

    Methods:
    - assigned_tasks(): Returns the tasks assigned to the user. It filters the
    `Task` model based on the user as the assignee.

    Example usage:
        user_profile = UserProfile.objects.get(user=user)
        assigned_tasks = user_profile.assigned_tasks()

    Note: This class should be used in conjunction with Django's User model for user authentication and authorization.
    """
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
