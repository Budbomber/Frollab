from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'owner', 'status', 'deadline_date', 'deadline_time')
    list_filter = ('owner', 'status')
    search_fields = ('title', 'description', 'owner', 'status', 'deadline_date', 'deadline_time')


admin.site.register(Task, TaskAdmin)
