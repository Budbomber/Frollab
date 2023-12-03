from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'status', 'deadline')
    list_filter = ('owner', 'status', 'deadline')
    search_fields = ('title', 'description', 'owner', 'status', 'deadline')


admin.site.register(Task, TaskAdmin)
