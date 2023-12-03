from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from apps.users.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login.html'), name='logout'),
    path('signup/', signup, name='signup'),
]
