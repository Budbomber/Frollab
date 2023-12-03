from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from apps.communication.models import Message
from apps.task_management.models import Task
from apps.users.models import UserProfile


# Register your models here.


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_task_count')

    def get_task_count(self, obj):
        return Task.objects.filter(owner=obj).count()

    get_task_count.short_description = 'Task Count'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
