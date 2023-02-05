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
from admin_custom.models import *
from cart.models import *
from .models import *
from cart.views import _cart_id
from wishlist.models import Wishlist
# Create your views here.
# def check_order_offers():
#     print('this is offer price check functionality')
#     #offers = Cat_Off.objects.all()
#     products = Product.objects.all()
#     #for off in offers:
#     for product in products:
#         #if off.category == product.Category_id:
#         if product.is_offers:
#             price = product.price - product.offer
#             #product.save()
#            # print(f"{off.category} - {product.Category_id} :-: price = {product.price} offers - {off.offers} offerprice {product.is_offers}")
def error_404_view(request, exception):
    return render(request,'error_404.html')


def index(request):
    #product = get_object_or_404(Product, id)
    #check_order_offers()
    
    product= Product.objects.all().order_by('-updated_at')
    products= Product.objects.filter(is_offer=True)
    
    for pro in products:
        if pro.is_offer:
            pro.offered_price = pro.price - pro.offer
            pro_price=pro.offered_price
            pro.save()
    #pro= Product.objects.filter(is_offer=True).first()

    # print(pro)
    
    #for i in range(1,pro):
    #print(i)
    # product_off= Product.objects.get(is_offer=True)
    # if product_off.is_offer:
    #     pro_price = product_off.price-product_off.offer
    context = {
        #'pro_price':pro_price,
        'product': product,
        'products': products,
        'banner':Banner.objects.all(),
    }
    return render(request, 'home.html', context)

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
    prod=None
    price_min = request.GET.get('price_min')
    print(price_min)
    price_max = request.GET.get('price_max')
    print(price_max)


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
        
    products = Product.objects.all().filter(is_available=True)
    if price_min:
        prod = products.filter(price__gte=price_min)
        product_count = prod.count()
        print(product_count)
    if price_max:
        prod = products.filter(price__lte=price_max)
        product_count = prod.count()
        print(product_count)

    context = {
        'prod':prod,
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store.html', context)

def product_detail(request,category_slug,product_slug):
    """   try:
       single_product = Product.objects.get(category__cat_slug=category_slug,slug=product_slug)
       #in_cart= CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
   except Exception as e:
       raise e
   product_gallery = ProductGallery.objects.filter(product_id=single_product)
   context ={
       'single_product':single_product,
       #'in_cart':in_cart,
       'product_gallery':product_gallery,
       
   } """
    print(category_slug)
    print(product_slug)
    number=(5,4,3,2,1)
    single_product = Product.objects.get(category__cat_slug=category_slug,slug=product_slug)
    in_cart= CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
    product_gallery = ProductImage.objects.filter(product_id=single_product)
    wishlist_items=None
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user, product=single_product).exists()
    

    context = {
        'number':number,
        'single_product':single_product,
        'in_cart':in_cart,
        'product_gallery':product_gallery,
        'wishlist_items': wishlist_items
    }
    
    return render(request, 'product_detail.html',context)


def search(request):
    keyword=None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(Q(product_desc__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
            context={
                'products':products,
                'product_count':product_count,
                'keyword':keyword,
            }
            # print(keyword)
        else:
            print(keyword)
            return redirect('home')
    return render(request, 'store.html',context)
