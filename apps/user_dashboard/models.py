from django.db import models
from django.conf import settings


# Create your models here.

class DashboardSetting(models.Model):
    """
    DashboardSetting class

    This class represents the dashboard settings for a user.

    Attributes:
    - user (models.OneToOneField): The user associated with the dashboard settings.
    - layout_preferences (dict): The layout preferences for the user's dashboard.

    Methods:
    - __str__: Returns a string representation of the dashboard settings.

    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layout_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user}\'s Dashboard Settings'
