from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User,OTP
import string
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from admin_custom.forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import pyotp
import random
from django.views.decorators.cache import never_cache
# Create your views here.

def admin_login(request):
    if request.user.is_authenticated: 
         return redirect('admin_dash')
    else:
        if request.method == 'POST':
            email  = request.POST['email']
            password = request.POST['password']
            try:
                User.objects.get(email=email,is_staff = True)
                admin = authenticate(email = email, password = password)
                if admin is not None:
                    login(request,admin)
                    return redirect('admin_dash')
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
            if user is not None:   
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, "Invalid password")
                #messages.error(request, "This account is blocked by admin")
                return redirect('login') 
    return render(request,"login.html")


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
                otp = generate_otp()
                print(otp)
                expiration_time = timezone.now() + timezone.timedelta(minutes=5)
                OTP.objects.create(otp=otp, expiration_time=expiration_time, user=user)
                send_mail(
                'OTP for Signup Verification',
                'Your OTP is {}. It will expire in 3 minutes.'.format(otp),
                'mithuncy65@gmail.com',
                [user.email],
                fail_silently=False,
                )
                return redirect('verify_otp')
            
                
        else:
            form=UserForm()
        context ={
            'form':form
        }

    return render(request,"register.html", context)
#FOR GENERATE OTP
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))
    #return ''.join([str(random.randint(0.9)) for i in range(6)])
""" def user_create(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=UserForm()
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
          
            form.save()
            email = form.cleaned_data.get('email')
            pwd = form.cleaned_data.get('password')
            user=authenticate(email=email,password=pwd)
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'register.html',{'form':form})  """
    
""" def admin_logout(request):
    try:
        logout(request)
    except:
        pass
    return redirect('login') """
    
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            otp_obj = OTP.objects.get(otp=otp, expiration_time__gt=timezone.now())
            user = otp_obj.user
            user.is_active = True
            user.save()
            """ login(request, user)
            return redirect('home') """
            messages.success(request, 'Profile created successfully')
            return redirect('login') 
        except OTP.DoesNotExist:
            return render(request, "verify_otp.html", {'error': 'Invalid or expired OTP'})
    return render(request, "verify_otp.html")


def admin_logout(request):
    
    logout(request)
    
    return redirect('admin_login')

@login_required(login_url ='login')
def logoutUser(request):
    logout(request)
    return redirect('home')
    """  if 'email' in request.session:
        request.session.flush() """
        
#def forgotPassword(request):
    #return render(request, 'forgotpass.html')