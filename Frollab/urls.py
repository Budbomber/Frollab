from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from apps.communication.views import view_message, delete_message, compose_message, mark_message_as_read
from apps.task_management import views
from apps.users.views import signup, edit_profile, view_profile
from apps.file_sharing.views import upload_file, file_list, delete_file
from apps.file_sharing.views import download_file
from apps.user_dashboard.views import Dashboard
from apps.users.views import logout_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='signup.html'), name='login'),
    path('logout/', logout_request, name='logout_request'),
    path('signup/', signup, name='signup'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('files/upload/', upload_file, name='upload_file'),
    path('files/', file_list, name='file_list'),
    path('files/download/<int:file_id>/', download_file, name='download_file'),
    path('files/delete/<int:file_id>/', delete_file, name='delete_file'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/view', view_profile, name='view_profile'),
    path('message/<int:message_id>/', view_message, name='view_message'),
    path('message/<int:message_id>/delete/', delete_message, name='delete_message'),
    path('compose/', compose_message, name='compose_message'),
    path('message/<int:message_id>/read/', mark_message_as_read, name='mark_message_as_read'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
