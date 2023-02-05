from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from cart.models import *
from .forms import *
import string
from order.models import *
from order.forms import *
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from admin_custom.forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

import random
from django.contrib import messages
from django.views.decorators.cache import never_cache
# Create your views here.

def admin_login(request):
    if request.user.is_authenticated: 
         return redirect('dashbord')
    
    else:
        if request.method == 'POST':
            email  = request.POST['email']
            password = request.POST['password']
            try:
                User.objects.get(email=email,is_staff = True)
                admin = authenticate(email = email, password = password)
                if admin is not None:
                    login(request,admin)
                    return redirect('dashbord')
                else:
                    messages.error(request, "Invalid password")
            except:
                messages.error(request,"You are not an admin")

    return render(request,"admin/admin_login.html")

@never_cache
def user_login(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        if request.method == 'POST':
            email  = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email = email, password = password)
            try:
                user= User.objects.get(email=email )
                if user.is_active and not user.is_block:
                    user = authenticate(email = email, password = password)
                    if user is not None:
                        login(request,user)
                        return redirect('home')
                    else:
                        messages.error(request, "Invalid password")
                else:
                    messages.error(request, "This account is blocked by admin")
            except:
                messages.error(request, "Invalid email")
    return render(request,"login.html")

def otp_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            if User.objects.filter(email__iexact=request.POST['email']).exists():
                email=email__iexact=request.POST['email']
                print(email)
                user = User.objects.filter(email=email).first()
                otp = generate_otp()
                print(otp)
                expiration_time = timezone.now() + timezone.timedelta(minutes=1)
                print(user)
                #print(OTP.objects.create(otp=otp, expiration_time=expiration_time, user=user))
                OTP.objects.create(otp=otp, expiration_time=expiration_time, user=user)
                try:
                    print('hello')
                    send_mail(
                    'OTP for Signup Verification',
                    'Your OTP is {}. It will expire in 3 minutes.'.format(otp),
                    'mithuncy65@gmail.com',
                    [user.email],
                    fail_silently=False,
                    )
                    print('hello')
                    return render(request, "verify_otp.html",{'expiration_time':expiration_time})
                except:
                    messages.error(request,"OTP send failed")
            else:
                messages.error(request,"Invalid email")
    return render(request, 'otp_login.html')

#FOR GENERATE OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))
    #return ''.join([str(random.randint(0.9)) for i in range(6)])

def user_create(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = form.cleaned_data['username']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,
                                    email=email,
                                    password=password)
                user.save()
                #create user profile
                profile                 = Address()
                profile.user_id         = user.id
                #profile.profile_picture = '/default/default-user.png'
                profile.save()
                otp = generate_otp()
                print(otp)
                expiration_time = timezone.now() + timezone.timedelta(minutes=3)
                OTP.objects.create(otp=otp, expiration_time=expiration_time, user=user)
                send_mail(
                'OTP for Signup Verification',
                'Your OTP is {}. It will expire in 3 minutes.'.format(otp),
                'mithuncy65@gmail.com',
                [user.email],
                fail_silently=False,
                )
                return render(request, "verify_otp.html",{'expiration_time':expiration_time})
        else:
            form=UserForm()
        context ={
            'form':form
        }

    return render(request,"register.html", context)



    
def verify_otp(request):
    if request.user.is_authenticated: 
         return redirect('home')
    else:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            print(otp)
            try:
                otp_obj = OTP.objects.get(otp=otp, expiration_time__gt=timezone.now())
                user = otp_obj.user
                print(user)
                if (user.is_verified != True):
                    user.is_active = True
                    user.save()
                login(request, user)
                OTP.objects.filter(user=user).delete()
                return redirect('home') 
            except OTP.DoesNotExist:
                return render(request, "verify_otp.html", {'error': 'Invalid or expired OTP'})
    return render(request, "verify_otp.html")


def resend_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email__iexact=email).exists():
            user = User.objects.filter(email=email).first()
            otp = generate_otp()
            expiration_time = timezone.now() + timezone.timedelta(minutes=5)
            OTP.objects.create(otp=otp, expiration_time=expiration_time, user=user)
            try:
                send_mail(
                'OTP for Signup Verification',
                'Your OTP is {}. It will expire in 3 minutes.'.format(otp),
                'mithuncy65@gmail.com',
                [user.email],
                fail_silently=False,
                )
                messages.success(request, 'OTP sent successfully')
                return redirect('verify_otp')
            except:
                messages.error(request, 'OTP send failed')
        else:
            messages.error(request, 'Invalid email')
    return render(request, 'otp_login.html')


def admin_logout(request):
    
    logout(request)
    
    return redirect('admin_login')

@login_required(login_url ='login')
def logoutUser(request):
    logout(request)
    return redirect('home')
    """  if 'email' in request.session:
        request.session.flush() """
    
    
@login_required(login_url = 'login')
def dashboard(request):
    orders       = Order.objects.order_by('-created_at').filter(user_id = request.user.id, is_ordered=True)
    orders_count = orders.count()
    
    print(request.user.id)
    
    context = {
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)
@never_cache
@login_required(login_url='login')   
def my_orders(request):
    orders = Order.objects.filter(user = request.user, is_ordered = True).order_by('-created_at')
    order = Order.objects.filter(is_ordered = False)
   
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)

@login_required(login_url='login')
@never_cache
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)  #orderproduct referred here in models
   
    order = Order.objects.get(order_number=order_id)
    used_coupon =UsedCoupon.objects.filter(user=request.user)
    print(used_coupon is None)
    if used_coupon.exists:
        coupon=None
    else:
        coupon=used_coupon.get(user=request.user)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    # #coupon = CouponDetail.objects.filter(user=request.user)
    # for i in coupon:
    #     coupon=i
    refund_form = RefundForm()    
    order_items = OrderProduct.objects.filter(order = order)
    if order.is_ordered == False:
        response = redirect('my_orders')
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
        'coupon':coupon,
        'refund_form':refund_form,
     }
    return render(request, 'accounts/order_detail.html', context)

@login_required(login_url='login')
def edit_profile(request):
        print(Address)
        #userprofile=Address.objects.get(user=request.user)
        if request.method == 'POST':
            user_form = UserProfileForm(request.POST, instance=request.user)
            print(user_form.errors)
            print(profile_form.errors)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('edit_profile')
        else:
            user_form = UserProfileForm(instance=request.user)
        context = {
            'user_form': user_form,
        }
        return render(request, 'accounts/edit_profile.html', context)
def user_address_check(request):
    user_id = User.objects.get(email = request.user)
    current_user_address = Address.objects.filter(user_id = user_id.pk)
    return render(request,'accounts/useraddresscheck.html',{'current_user_address':current_user_address})




def user_address_edit(request,id):
    current_user_address = Address.objects.get(id=id)
    edituseraddress = AddressForm(request.POST or None,instance=current_user_address)
    if request.POST:
        edituseraddress.save()
        return redirect('user_address_check')
    return render(request,'accounts/editaddress.html',{'forms':edituseraddress})

