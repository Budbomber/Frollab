from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.users.models import UserProfile


class SignUpForm(UserCreationForm):
    """
    The `SignUpForm` class is a form used for user registration. It extends the `UserCreationForm` provided by Django
    and adds additional fields for username, email, password1, and password2.

    Attributes:
        Meta (class): An inner class that specifies the metadata for the `SignUpForm` class, including the `model`
        and `fields`.

        model (User): The model used for user registration, which in this case is the `User` model provided by Django.

        fields (tuple): The fields to be included in the `SignUpForm` class, which include 'username', 'email',
        'password1', and 'password2'.

    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    """

    The UserProfileForm class is a form that is used to handle user profile information.
    It is a subclass of django's ModelForm.

    Attributes:
        model (UserProfile): The UserProfile model that the form is associated with.
        fields (list): The fields of the UserProfile model that are included in the form.

    Usage:
        To use the UserProfileForm class, create an instance of it and pass in the necessary arguments.

    Example:
        form = UserProfileForm()

    """

    class Meta:
        model = UserProfile
        fields = ['organization', 'job_title', 'profile_picture', 'bio', 'location', 'contact_number', 'website_url']


