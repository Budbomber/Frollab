from django.shortcuts import render
from django.views import View

from apps.file_sharing.models import SharedFile
from apps.task_management.models import Task


class Dashboard(View):
    @staticmethod
    def get(request):
        user_tasks = Task.objects.filter(owner=request.user)
        user_files = SharedFile.objects.filter(owner=request.user)

        context = {
            'user_tasks': user_tasks,
            'user_files': user_files,
        }

        return render(request, 'dashboard.html', context)
