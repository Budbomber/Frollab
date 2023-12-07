from django.db import models
from django.conf import settings


# Create your models here.

class DashboardSetting(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    layout_preferences = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.user}\'s Dashboard Settings'


class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    date_created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
