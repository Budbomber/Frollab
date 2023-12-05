from django import forms
from apps.communication.models import Message


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'subject', 'message']
