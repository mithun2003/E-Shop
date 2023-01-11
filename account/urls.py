from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_create, name='register'),
    path('logout/', views.logoutUser, name='logout'),

]