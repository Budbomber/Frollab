from django import forms
from django.contrib.auth.models import User

from apps.communication.models import Message


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message', 'subject', 'message']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'message']

    def clean_receiver(self):
        receiver_username = self.cleaned_data.get('receiver')
        try:
            receiver = User.objects.get(username=receiver_username)
            return receiver
        except User.DoesNotExist:
            raise forms.ValidationError('User does not exist')

    def save(self, commit=True):
        message = super(MessageForm, self).save(commit=False)
        receiver_username = self.cleaned_data['receiver']
        message.receiver = User.objects.get(username=receiver_username)
        if commit:
            message.save()
        return message
