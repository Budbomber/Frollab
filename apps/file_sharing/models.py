from django.db import models
from django.conf import settings


# Create your models here.

class SharedFile(models.Model):
    """

    This class represents a shared file.

    Attributes:
        title (CharField): The title of the file.
        file (FileField): The uploaded file.
        owner (ForeignKey): The owner of the file.
        uploaded_at (DateTimeField): The datetime when the file was uploaded.

    """
    title = models.CharField(max_length=100, default='default title')
    file = models.FileField(upload_to='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File {self.title} This File was uploaded at: {self.uploaded_at} by {self.owner}'
