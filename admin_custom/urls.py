from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [   
    #path('admin_dashboard/', views.admin_dashboard, name='admin_dash'),
    path('admin_dashboard/dashboard',views.dashboard,name='dashbord'),
    
    path('admin_dashboard/category', views.category_list, name='category_list'),
    path('admin_dashboard/category_create', views.category_create, name='category_create'),
    path('admin_dashboard/category_update/<category_id>/', views.category_update, name='category_update'),
    path('admin_dashboard/<category_id>/category_delete', views.category_delete, name='category_delete'),
    
    path('admin_dashboard/coupon', views.coupon_list, name='coupon_list'),
    path('admin_dashboard/coupon_create', views.coupon_create, name='coupon_create'),
    path('admin_dashboard/coupon_update/<coupon_id>/', views.coupon_update, name='coupon_update'),
    path('admin_dashboard/<coupon_id>/coupon_delete', views.coupon_delete, name='coupon_delete'),

    
    path('admin_dashboard/variation', views.variation_list, name='variation_list'),
    path('admin_dashboard/variation_create', views.variation_create, name='variation_create'),
    path('admin_dashboard/<variation_id>/variation_delete', views.variation_delete, name='variation_delete'),
    
    
    path('admin_dashboard/product', views.product_list, name='product_list'),
    path('admin_dashboard/product_create', views.product_create, name='product_create'),
    path('admin_dashboard/<product_id>/product_update', views.product_update, name='product_update'),
    path('admin_dashboard/product_delete', views.product_delete, name='product_delete'),
    
    
    path('user/',views.user_table,name='user_table'),
    path('user/block',views.user_block,name='user_block'),
    path('unblock/<id>/',views.user_unblock,name='user_unblock'),
    
    path('admin_dashboard/order', views.order_list, name='order_list'),
    path('admin_dashboard/<order_number>/order_update', views.order_update, name='order_update'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('export/sales', views.export_sales_xls, name='export_sales'),

    
    path('banner/',views.banners,name='banners'),
    path('addbanner/',views.add_banner,name='add_banner'),
    path('delbanner/<banner_id>',views.banner_delete,name='banner_delete'),
    
    
    path('history',views.order_history,name='order_history'),
    
    





]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
