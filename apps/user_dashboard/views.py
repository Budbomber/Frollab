from django.shortcuts import render, redirect
from django.views import View

from apps.communication.models import Message
from apps.file_sharing.models import SharedFile
from apps.task_management.models import Task
from apps.task_management.views import TaskForm


class Dashboard(View):
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
