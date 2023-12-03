from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'created_at', 'updated_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'subject', 'message')

    def get_read_status(self, obj):
        return 'Read' if obj.is_read else 'Unread'

    get_read_status.short_description = 'Read Status'


admin.site.register(Message, MessageAdmin)
