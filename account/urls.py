from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('otp_login/', views.otp_login, name='otp_login'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_create, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),

    
    path('dashboard/', views.dashboard, name="dashboard"),
    path('my_orders/',views.my_orders, name='my_orders'),
    path('order_detail/<int:order_id>/',views.order_detail, name='order_detail'),
    path('edit_profile/',views.edit_profile, name='edit_profile'),


    path('address/',views.user_address_check,name="user_address_check"),
    path('editaddress/<int:id>/',views.user_address_edit,name='user_address_edit')
    #path('forgotpassword', views.forgotPassword, name='forgotpassword'),
    

]