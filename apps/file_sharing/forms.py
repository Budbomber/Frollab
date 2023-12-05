from django import forms
from .models import SharedFile


class FileUploadForm(forms.ModelForm):
    """
    A form class for uploading files.

    Attributes:
        Meta (Meta): A nested class specifying information about the form's behavior.

    """
    class Meta:
        model = SharedFile
        fields = ['title', 'file']
