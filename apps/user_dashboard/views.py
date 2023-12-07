from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.communication.models import Message
from apps.file_sharing.models import SharedFile
from apps.task_management.models import Task
from apps.task_management.views import TaskForm
from apps.user_dashboard.models import Alert

DASHBOARD_HTML_PATH = 'dashboard.html'


class Dashboard(LoginRequiredMixin, View):

    @staticmethod
    def _get_user_data(request):
        user = request.user
        user_tasks = Task.objects.filter(owner=user)
        user_files = SharedFile.objects.filter(owner=user)
        user_messages = Message.objects.filter(receiver=user)
        alerts = Message.objects.filter(receiver=user, is_read=False)
        return user_tasks, user_files, user_messages, alerts

    def get(self, request):
        user_tasks, user_files, user_messages, alerts = self._get_user_data(request)
        context = {
            'user_tasks': user_tasks,
            'task_form': TaskForm(),
            'user_files': user_files,
            'user_messages': user_messages,
            'alerts': alerts,
        }
        return render(request, DASHBOARD_HTML_PATH, context)

    def post(self, request):
        user = request.user
        form = TaskForm(request.POST)
        user_tasks, _, _, _ = self._get_user_data(request)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = user
            new_task.save()
            return redirect('dashboard')
        return render(request, DASHBOARD_HTML_PATH, {'user_tasks': user_tasks, 'task_form': form})

    @staticmethod
    def dashboard(request):
        user = request.user
        alerts = Alert.objects.filter(user=user, read=False)
        return render(request, DASHBOARD_HTML_PATH, {'alerts': alerts})
