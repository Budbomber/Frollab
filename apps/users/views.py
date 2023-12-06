from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserProfileForm
from .models import UserProfile


# Create your views here.
def signup(request):
    """
    Handles the signup process for new users.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response object containing the rendered template.

    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save the user's form data to the database.
            form.save()
            # Redirect to the home page.
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def logout_request(request):
    """

    This method handles the logout functionality for a logged-in user.

    Parameters:
    - request (object): The HTTP request object.

    Returns:
    - If the request method is 'POST':
        - Redirects the user to the login page after logging out successfully.
    - If the request method is not 'POST':
        - Renders the 'logout.html' template.

    Example Usage:
    logout_request(request)

    """
    if request.method == 'POST':
        logout(request)
        messages.info(request, "Logged out successfully!")
        return redirect('login')
    return render(request, 'logout.html')


@login_required
def edit_profile(request):
    """

    Edit Profile

    This method allows a user to edit their profile information. The method is accessed through a POST request to the
     '/edit_profile/' URL and is only available to logged-in users.

    Parameters:
    - request: The HTTP request object.

    Example usage:
    edit_profile(request)

    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    """

    View the user profile.

    This method is a view function that displays the user's profile. It is only accessible to authenticated users,
    meaning users who have already logged in. The method retrieves the user's profile from the database and renders
    the view_profile.html template with the profile data.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered template response that displays the user's profile.

    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'view_profile.html', {'profile': profile})
