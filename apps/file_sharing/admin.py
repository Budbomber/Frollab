from django.contrib import admin
from .models import SharedFile


# Register your models here.

class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_link', 'owner', 'uploaded_at')
    list_filter = ('owner', 'uploaded_at')
    search_fields = ('title', 'owner__username')

    def file_link(self, obj):
        if obj.file:
            return "<a href='%s'>download</a>" % (obj.file.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True
    file_link.short_description = 'File Download'


admin.site.register(SharedFile, SharedFileAdmin)
