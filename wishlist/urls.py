from django.urls import path
from .views import view_wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('', view_wishlist, name='wishlist'),
    path('wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
