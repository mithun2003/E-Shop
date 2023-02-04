from django.shortcuts import render,redirect
from cart.models import *
from .forms import OrderForm
from .models import Order,Payment,OrderProduct 
from account.models import * 
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http import HttpResponseRedirect
from cart.views import _cart_id
from django.http import HttpResponse,JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from admin_custom.models import Product
import random
# Create your views here.
def Payments(request):
    body = json.loads(request.body)
    #print(body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(request.user)
    
    
    #STORE TRANSACTION DETAILS
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    print("saved")
    
    order.payment = payment
    order.is_ordered=True
    order.status='Placed'
    order.save()
    print("order")
    print(order)
    
    if order.status=='Pending':
        order.status='Canceled'
        order.save()
    #MOVE THE CART ITEMS TO ORDER PRODUCT TABLE
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=payment
        orderproduct.user_id=item.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


        #REDUCE THE QUANTITY OF THE SOLD PRODUCTS
        product=Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()
    
    #CLEAR CART ITEM
    cart = Cart.objects.filter(cart_id=_cart_id(request))
    cart.delete()
    CartItem.objects.filter(user=request.user).delete()
    #SENT EMAIL TO USER
    
    email_subject = 'Thank You for your order'
    message = render_to_string('order/order_received_email.html',{
        'user': request.user,
        'order':order,
    })
    to_mail = request.user.email 
    send_mail = EmailMessage(email_subject,message,to=[to_mail])
    send_mail.send()
    
    #SEND ORDER SUCCESSFUL PAGE
    data={
        'order_number': order.order_number,
        'transID':payment.payment_id,
    }
    
    
    return JsonResponse(data)
   
    #return render(request, 'order/cod_pay.html', {'cod_payment': cod_payment})
    #return render(request, 'order/payment.html')

@never_cache
def place_order(request,total=0,quantity =0,order=None,coupon_obj=None):
    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    carts=Cart.objects.filter(cart_id=_cart_id(request)).first()
    cart=CartItem.objects.get(user=current_user,cart=carts)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect('store')
    
    data = Order()

    tax=0
    grand_total=0
    for cart_item in cart_item:
        #total+=(cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity
        if cart_item.product.is_offer:
            total+=(cart_item.product.offered_price * cart_item.quantity)
        else:
            total+=(cart_item.product.price * cart_item.quantity)
            
        data.product_id=cart_item.product_id
        data.quantity=cart_item.quantity
        data.product_price=cart_item.product.price
        data.save()
    if cart.coupon:
            if cart.coupon.min_amount<cart.sub_total():
                total=total-cart.coupon.amount

    tax=(0.02)*(total) 
    grand_total=total+tax
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        #print(form)
        print (form.errors)
        if form.is_valid():
            print('HELLO')
            address = Address.objects.get(pk = request.POST.get('address'))
            #store all the billing info in table
            data.user=current_user
            data.address=address

            data.order_note=form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            
            #generate order id
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number=current_date + str(data.id)
            data.order_number = order_number
            data.save()  
            
            order = Order.objects.get(user=current_user,is_ordered= False,order_number = order_number)
           
            #user = User.objects.get(user=current_user)
            #address = Address.objects.get(user_id=request.user.id)
        context ={
            'order':order,
            'cart_item':cart_item,
            'total':total,
            'cart':cart,
            'tax':tax , 
            'grand_total':grand_total,
                #'user':user,
                #'address':address,         
            }
            
        return render(request,'order/payment.html',context)     
    else:
        return redirect('checkout')
    
def cancel_payment(request):
    order_number = request.GET.get('order_number')
    order = Order.objects.get(order_number=order_number)
    order.status = 'Canceled'
    order.save()
    return redirect('cart')

def apply_coupon(request):
    if request.method == 'POST':
        code =  request.POST['coupon']
        try:
            coupon = Coupon.objects.get(code__iexact = code)
            carts=Cart.objects.filter(cart_id=_cart_id(request)).first()
            cart = CartItem.objects.get(user = request.user,cart=carts)
           
            if coupon.used<coupon.max_use:
                coupon.is_expired=True
                coupon.save()
            # if cart.coupon.used:
            #     print(cart.get_cart_total())
            #     messages.warning(request,'Coupon Applied Already')
            #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if cart.product.is_offer:
                messages.warning(request,'Coupon Cannot Apply')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if cart.coupon:
                print(cart.get_cart_total())
                messages.warning(request,'Coupon Applied')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if cart.get_cart_total() < coupon.min_amount:
                print(cart.get_cart_total())
                messages.warning(request, f'Amount should be greater than { coupon.min_amount }')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            if coupon.is_expired :
                messages.warning(request,'Coupon expired')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
        except ObjectDoesNotExist:
             messages.warning(request,'Invalid Coupon.')
             return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        try:
            used_coupon = UsedCoupon.objects.get(user = request.user,coupon = coupon)
            if used_coupon.status:
                messages.warning(request,'Coupon Already Used')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                used_coupon.status = True
                used_coupon.save()
        except ObjectDoesNotExist:
            used_coupon = UsedCoupon.objects.create(user = request.user,coupon = coupon)

        coupon.used += 1
        coupon.save()
        cart.coupon = coupon
       
        cart.save()
        

        messages.success(request, 'Coupon applied')        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_coupon(request, cart_id):
    cart =  CartItem.objects.get(id = cart_id)
    coupon = cart.coupon
    coupon.used -= 1
    coupon.save()
    
    used_coupon = UsedCoupon.objects.get(user = request.user,coupon = coupon)
    used_coupon.status = False
    used_coupon.save()

    cart.coupon = None
    cart.save()

    messages.success(request, 'Coupon removed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
@never_cache
def Success(request,order_number):
    print(order_number)
    transID = request.GET.get('payment_id')
    coupon=UsedCoupon.objects.filter(user=request.user)
    try:
        print("1")
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        print("2")
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        print("3")
        
        subtotal = 0
        for i in ordered_products:
            print("4")
            if i.product.is_offer:
                print("5")
                subtotal+=i.product.offered_price * i.quantity
                print("6")
            else:
                print("7")
                subtotal += i.product_price * i.quantity
                print("8")
        if order.payment.payment_method=='Cash on Delivery':
            payment=order.payment
        else:
            payment = Payment.objects.get(payment_id=transID)
        print("9")
        
        context = {
            'order':order,
            'ordered_products':ordered_products,
            'order_number':order.order_number,
            'transID':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
            'coupon':coupon,
            
        }
        return render(request,'order/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('place_order')
@never_cache
def cod(request,order_number):
    if request.method == 'POST':
        order = Order.objects.get(user=request.user, is_ordered=False,order_number=order_number)
        # Store transaction details inside Payment model
        payment = Payment(
            user = request.user,
            #payment_id = random.randint(111111,999999),
            payment_method = "Cash on Delivery",
            amount_paid = order.order_total,
            status = "Placed",
        )
        payment.save()

        order.payment = payment
        order.status='Placed'

        order.is_ordered = True
        order.save()

        # Move the cart items to Order Product table
        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()


            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()

        # Clear cart
        cart = Cart.objects.filter(cart_id=_cart_id(request))
        cart.delete()
        CartItem.objects.filter(user=request.user).delete()
        
        
        order_product = OrderProduct.objects.get(user=request.user, order__is_ordered=True,order__order_number=order_number)
        order_details = {
            'order':order_product
        }
        # return render(request, 'order/cod_success.html',order_details)
    
        return redirect('success',order_number=order_number)
    else:
        return redirect('cart')

