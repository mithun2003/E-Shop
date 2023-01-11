from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from datetime import date
from .forms import *
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from .models import *
# Create your views here.
""" def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(
                    request, 'Profile created successfully' + user)
                return redirect('login')
        context = {'form': form}
        return render(request, 'register.html', context) """
""" 
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
          
            form.save()
            name = form.cleaned_data.get('name')
            pwd = form.cleaned_data.get('password1')
            user=authenticate(name=name,password=pwd)
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occurred during registration')
    return render(request,'register.html',{'form':form}) 
 """
def index(request):
    #product = get_object_or_404(Product, id)
    today = date.today()
    if 'name':
        dict_docs = {
            'product': Product.objects.all().order_by('-updated_at'),
            'banner':Banner.objects.all(),
        }
        return render(request, 'home.html', dict_docs)
    return redirect('login')

""" 
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method=="POST":
        name=request.POST.get('username')
        password=request.POST.get('password')
             try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            print("hello user")
            return redirect('home')
        else:
            messages.error(request,'Username or password incorrect')
            
    return render(request,'login.html')  """

def logoutUser(request):
    if 'username' in request.session:
        request.session.flush()
    logout(request)
    return redirect('home')

def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, cat_slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('-updated_at')
        paginator=Paginator(products, 6)
        page= request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('-updated_at')
        paginator=Paginator(products, 6)
        page= request.GET.get('page')
        paged_products = paginator.get_page(page) #6 products will be shown in the first page
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__cat_slug=category_slug,slug=product_slug)
        #in_cart= CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    except Exception as e:
        raise e
    product_gallery = ProductGallery.objects.filter(product_id=single_product)
    context ={
        'single_product':single_product,
        #'in_cart':in_cart,
        'product_gallery':product_gallery,
        
    }
    
    return render(request, 'product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(product_desc__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            context={
                'products':products,
                'product_count':product_count,
            }
        else:
            return redirect('home')
    return render(request, 'store.html',context)
