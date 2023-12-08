from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import SignUpForm, UserProfileForm
from .models import UserProfile


# Helper method to get user profile
def get_user_profile(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return profile


# Helper method to handle form processing
def handle_form(request, form_class, instance=None):
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return True, form
    else:
        form = form_class(instance=instance)
    return False, form


def signup(request):
    is_saved, form = handle_form(request, SignUpForm)
    if is_saved:
        return redirect('login')
    return render(request, 'signup.html', {'form': form})


@require_POST
@login_required
def logout_request(request):
    logout(request)
    return redirect('login')


@login_required
def edit_profile(request):
    profile = get_user_profile(request.user)
    is_saved, form = handle_form(request, UserProfileForm, instance=profile)
    if is_saved:
        return redirect('view_profile')
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def view_profile(request):
    profile = get_user_profile(request.user)
    return render(request, 'view_profile.html', {'profile': profile})
