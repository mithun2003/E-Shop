
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.shortcuts import get_object_or_404
from admin_custom.models import Product
from django.contrib import messages



@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {'wishlist_items': wishlist_items}
    return render(request, 'wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    existing_wishlist_item = Wishlist.objects.filter(user=request.user, product=product).exists()
    if existing_wishlist_item:
        # if the product is already in the wishlist, notify user
        messages.info(request, 'Product already in your wishlist')
    else:
        # if the product is not in the wishlist, add it
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, 'Product added to your wishlist')   
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')
