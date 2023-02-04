from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/',views.Payments,name='payment'),
    path('success/<int:order_number>',views.Success,name='success'),
    path('cancel_order/<str:order_no>', views.cancel_order, name="cancel_order"),
    path('cod/<int:order_number>',views.cod,name='cod'),
    path('apply_coupon', views.apply_coupon ,name="apply_coupon"),
    path('remove_coupon/<str:cart_id>', views.remove_coupon, name="remove_coupon"),

]