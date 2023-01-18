from django.shortcuts import render,redirect
from cart.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct 
import datetime
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import json
# Create your views here.
def Payment(request):
    
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    #STORE TRANSACTION DETAILS
    payment=Payment(
    payment_id = body['transID'],
    payment_method = body['payment_method'],
    amount_paid = order.order_total,
    status=body['status'],
    )
    payment.save()
    
    order.payment = payment
    order.is_ordered=True
    order.save()
    
    
    #MOVE THE CART ITEMS TO ORDER PRODUCT TABLE
    
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id=order.id
        orderproduct.payment=order.id
        orderproduct.user_id=item.user.id
        orderproduct.product_id=item.product_id
        orderproduct.quantity=item.quantity
        orderproduct.product_price=item.product.price
        orderproduct.ordered=True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=Orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()


    #REDUCE THE QUANTITY OF THE SOLD PRODUCTS
    
    
    #CLEAT CARTS
    
    
    #SENT EMAIL TO USER
    
    
    return render(request, 'order/cod_pay.html', {'cod_payment': cod_payment})
    #return render(request, 'order/cod_pay.html')

@never_cache
def place_order(request,total=0,quantity =0):
    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect('store')
    
    tax=0
    grand_total=0
    for cart_item in cart_item:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity+= cart_item.quantity
    tax=(0.02)*(total) 
    grand_total=total+tax
    
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        #print(form)
        print (form.errors)
        if form.is_valid():
            print('HELLO')
            #store all the billing info in table
            data = Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.pincode=form.cleaned_data['pincode']
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
            
            context ={
                'order':order,
                'cart_item':cart_item,
                'total':total,
                'tax':tax , 
                'grand_total':grand_total,         
                }
            
            return render(request,'order/payment.html',context)     
    else:
        return redirect('checkout')
@never_cache

def Success(request, order = None):
    """ if request.user.is_authenticated:
        order = Order.objects.filter(user = request.user).last()
        status='completed'
        payment=Payment.objects.create(status=status)
        payment.save()
    context = {
        "order": order
    } """
    return render(request,"order/success.html")

#how to do payment for an ecommerce website with django?
layout: 'horizontal'



#Source: https://stackoverflow.com/questions/63965098







