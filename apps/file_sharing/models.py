from django.db import models
from django.conf import settings


# Create your models here.

class SharedFile(models.Model):
    file = models.FileField(upload_to='shared_files')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shared_with')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    shared = models.BooleanField(default=False)
    shared_with_email = models.EmailField(max_length=254, blank=True, null=True)

    def __str__(self):
        return f'File {self.file.name} This File was uploaded at: {self.uploaded_at} by {self.owner}'
