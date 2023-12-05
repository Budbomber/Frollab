from django import forms
from django.contrib.auth.models import User

from apps.communication.models import Message


class ReplyForm(forms.ModelForm):
    """
       A form for replying to a message.

       Inherits from django.forms.ModelForm.

       Attributes:
           model (class): The model class to use for the form.
           fields (list): The list of fields to display in the form.

       """

    class Meta:
        model = Message
        fields = ['message', 'subject', 'message']


class MessageForm(forms.ModelForm):
    """
    The MessageForm class is a Django ModelForm that is used for creating and editing instances of the Message model.

    Attributes:
        - model (django.db.models.Model): The model that the form is associated with, in this case the Message model.
        - fields (list): The fields of the model that will be included in the form, in this case
         ['receiver', 'subject','message'].

    Methods:
        - clean_receiver: This method is used to clean and validate the receiver field. It retrieves the receiver
         username from the form's cleaned data, tries to retrieve the associated User instance from the database,
          and returns it if it exists. If the User does not exist, it raises a ValidationError with the message
           'User does not exist'.

        - save: This method is overridden from the parent class and is called when the form is saved. It retrieves
        the cleaned receiver username from the form's cleaned data and sets the message's receiver field to the
        associated User instance retrieved from the database. If the 'commit' parameter is True, it saves the message
        instance to the database. Finally, it returns the saved message instance.

    Note: This class requires the following imports to work properly:
        from django import forms
        from django.contrib.auth.models import User
        from apps.communication.models import Message
    """

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
