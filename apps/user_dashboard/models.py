from django.db import models
from django.conf import settings


# Create your models here.

class DashboardSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layout_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user}\'s Dashboard Settings'
