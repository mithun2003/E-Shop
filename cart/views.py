from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from admin_custom.models import *
from account.forms import *
from .models import *
from account.models import *
from django.core.exceptions import ObjectDoesNotExist
from admin_custom.models import Product
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from order.forms import *
from django.http import JsonResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 

@login_required(login_url='login')
def add_cart(request,product_id):
    current_user=request.user
    product= Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                print(key)
                print(request.POST[key])
                try:
                    variations = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variations)
                    print(variations)
                    print(product_variation)
                except:
                    pass
        
        is_cart_item_exist = CartItem.objects.filter(product=product, user=current_user).exists()
        print(is_cart_item_exist)
        if is_cart_item_exist:
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            if product.stock<=cart_item[0].quantity:
                messages.error(request,'Out of stock')
                return redirect('cart')
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation)
            print(id)
            print(ex_var_list)
            print(product_variation in ex_var_list)
            if product_variation in ex_var_list:
                #INCREASE CART ITEM QUANTITY
                print('PRODUCT')
               
                index=ex_var_list.index(product_variation)
                item_id = id[index]
                item= CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item= CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
  
        else:
            
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()
            cart_item = CartItem.objects.create(product=product,quantity=1,user=current_user,cart=cart)
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save() 
            cart_item = CartItem.objects.get(product=product,user=current_user,cart=cart)
      
        return redirect('cart')

#REMOVE CART ITEM

def remove_cart(request,product_id,cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart.delete()
        
    return redirect('cart')
   
def remove_cart_item(request,product_id,cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, user=request.user,id=cart_item_id)
    cart_item.cart.delete()
    cart_item.delete()
    # cart = Cart.objects.get(cart_id=_cart_id(request))
    # cart.delete()
    return redirect('cart')
    #request.session['cart_item'] = cart_item.count()
    #return redirect('cart')

@login_required(login_url='login')
def cart(request):
    total=0
    quantity =0  
    cart_items=None

    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        for cart_item in cart_items:
            product = Product.objects.get(pk = cart_item.product.id)
            if product.stock<cart_item.quantity:
                cart_item.delete()
                return redirect('cart')
            else:
                quantity+= cart_item.quantity       
                if cart_item.product.is_offer:
                    total+=(cart_item.product.offered_price * cart_item.quantity)
                else:
                    total+=(cart_item.product.price * cart_item.quantity)
        tax = (2/100)*(total) 
        tax = round(tax,2)
        grand_total=total+tax
        
    except ObjectDoesNotExist:
        pass
    
        
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        
    }

    return render(request, 'cart/cart.html',context)

@login_required(login_url='login')
def checkout(request,total=0,quantity =0,cart_items=None):
    address_form = AddressForm()
    user=request.user
    address=Address.objects.filter(user=request.user)

    #address=Address.objects.filter(user=request.user)
    #address=Address.objects.get(user=request.user)
    print(user)
    print(user.phone_number)
    #order_form = OrderForm(instance=address)
    #profile_form = OrderForm(instance=request.user)
    try:
        tax=0
        grand_total=0
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
            carts=Cart.objects.filter(cart_id=_cart_id(request)).first()
            print(carts)
            cart=CartItem.objects.all().get(user=request.user,cart=carts)
        for cart_item in cart_items:
            quantity+= cart_item.quantity                    
            if cart_item.product.is_offer:
                total+=(cart_item.product.offered_price * cart_item.quantity)
            else:
                total+=(cart_item.product.price * cart_item.quantity)     
        if cart_item.product.is_offer:
            pass
        else:
            if cart.coupon:
                if cart.coupon.used<cart.coupon.max_use:
                    cart.coupon.is_expired=True
                    cart.coupon.save()
                if cart.coupon.min_amount<cart.sub_total():
                    total=total-cart.coupon.amount
        tax=(0.02)*(total) 
        grand_total=total+tax

        #address = Address.objects.get(user = request.user)        # if request.method == 'POST':
        #     order_form = OrderForm(request.POST, instance=address)
        #     profile_form = OrderForm(request.POST, instance=request.user)
        #     print(order_form.errors)
        #     if order_form.is_valid():
        #         order_form.save()
        #         messages.success(request, 'Your profile has been updated.')
        #         return redirect('edit_profile')
        # else:
        #     order_form = OrderForm(instance=address)
        #     profile_form = OrderForm(instance=request.user)
    except ObjectDoesNotExist:
        print("ERROR")
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        # 'form':order_form,
        # 'user':profile_form,
        'address':address,
        'address_form':address_form,
        'cart':cart,
    }
    return render(request,'cart/checkout.html',context) 


def add_address(request):
    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            address_line_1 = address_form.cleaned_data['address_line_1']
            address_line_2 = address_form.cleaned_data['address_line_2']
            city = address_form.cleaned_data['city']
            state = address_form.cleaned_data['state']
            country = address_form.cleaned_data['country']
            pincode = address_form.cleaned_data['pincode']
            address = Address.objects.create(user = request.user, address_line_1 = address_line_1, address_line_2 = address_line_2,city = city,state=state, country = country, pincode = pincode)
    return redirect('checkout')

# Create your views here.


