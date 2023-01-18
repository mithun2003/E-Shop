from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/',views.Payment,name='payment'),
    path('success/',views.Success,name='success'),
]