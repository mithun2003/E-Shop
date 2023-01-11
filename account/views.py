from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .models import User

from django.contrib import messages
from django.core.mail import send_mail
from admin_custom.forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import pyotp
import random
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
                if username is None:
                    username = email.split("@")[0] 
                username = form.cleaned_data['username']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,phone_number=phone_number,
                                    email=email,
                                    password=password)
                user.save()
                messages.success(
                    request, 'Profile created successfully')
                return redirect('login') 
        context ={
            'form':form
        }

    return render(request,"register.html", context)

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
def admin_logout(request):
    
    logout(request)
    
    return redirect('admin_login')

@login_required(login_url ='login')
def logoutUser(request):
    logout(request)
    return redirect('home')
    """  if 'email' in request.session:
        request.session.flush() """