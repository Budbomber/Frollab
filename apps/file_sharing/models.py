from django.db import models
from django.conf import settings


# Create your models here.

class SharedFile(models.Model):
    title = models.CharField(max_length=100, default='default title')
    file = models.FileField(upload_to='shared_files')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File {self.title} This File was uploaded at: {self.uploaded_at} by {self.owner}'
