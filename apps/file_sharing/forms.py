from django import forms
from .models import SharedFile


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = SharedFile
        fields = ['title', 'file']
