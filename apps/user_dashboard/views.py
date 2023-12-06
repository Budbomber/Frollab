from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.communication.models import Message
from apps.file_sharing.models import SharedFile
from apps.task_management.models import Task
from apps.task_management.views import TaskForm


class Dashboard(LoginRequiredMixin, View):
    """
    The Dashboard class provides functionality for the user dashboard page.

    It includes methods for displaying and handling user tasks, shared files, and messages.

    Inherits:
        LoginRequiredMixin: A Django mixin to enforce authentication for accessing the dashboard.

    Methods:
        get: Handles GET requests and renders the dashboard page.
        post: Handles POST requests and adds a new task to the user's task list.
    """
    @staticmethod
    def get(request):
        user_tasks = Task.objects.filter(owner=request.user)
        user_files = SharedFile.objects.filter(owner=request.user)
        user_messages = Message.objects.filter(receiver=request.user)
        form = TaskForm()

        context = {
            'user_tasks': user_tasks,
            'task_form': form,
            'user_files': user_files,
            'user_messages': user_messages,
        }

        return render(request, 'dashboard.html', context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('dashboard')

        user_tasks = Task.objects.filter(owner=request.user)
        return render(request, 'dashboard.html', {'user_tasks': user_tasks, 'task_form': form})
