from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

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


@require_POST
@login_required
def logout_request(request):

    logout(request)
    return redirect('login')


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

    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None
    return render(request, 'view_profile.html', {'profile': profile})
