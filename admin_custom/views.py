from django.shortcuts import redirect, render
from .models import *
from account.models import User
#from order.models import Order, OrderItem
from .forms import *
#from order.forms import OrderForm
from django.contrib import messages
from django.template import loader
from django.template.defaultfilters import slugify
from .decorators import user_is_admin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Q
from django.db.models import Count
from django.http import HttpResponse
from django.conf import settings
import calendar

# Create your views here.
#=====CATEGORY=====
@user_is_admin
def category_list(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        categories = categories.filter(Q(category_name__icontains = keyword) )
    paginator = Paginator(categories, 8)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)
    content = {
        'categories': paged_categories
    }
    return render(request,"admin/category.html", content)
@user_is_admin
def category_create(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            messages.success(request, "Category Created")
            return redirect('category_list')
        else:
            messages.error(request,"Category creation failed ")

    context ={
        'category_form':form
    }

    return render(request,"admin/category_create.html", context)
@user_is_admin
def category_update(request, category_id):
    category = Category.objects.get(id = category_id)
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category Updated Successfully')
            return redirect(to='category_list')
    else:
        category_form = CategoryForm(instance=category)
        
    return render(request,"admin/category_update.html",  {'category_form': category_form})
@user_is_admin
def category_delete(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category.delete()
        render(request, 'admin/category.html')
    return redirect(to='category_list')
#=====END CATEGORY=====

#=====PRODUCT=====
@user_is_admin
def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        products = products.filter(Q(name__icontains = keyword) | Q(category__name__icontains = keyword) | Q(description__icontains = keyword)).order_by('-created')
    paginator = Paginator(products, 7)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    content ={
        'products': paged_products
    }
    return render(request,"admin/product.html", content)

@user_is_admin
def admin_dashboard(request):
    """ orders_month = Order.objects.annotate(month=ExtractMonth("created_at")).values("month").annotate(count=Count('id')).values('month','count')
    months=[]
    total_orders = []
    for order in orders_month:
        months.append(calendar.month_name[order['month']])
        total_orders.append(order['count'])
    orders = Order.objects.order_by('-created_at')[:2]
    users = User.objects.filter(is_staff = False, is_admin = False, is_superuser = False).order_by('-date_joined')[:5]
    context = {
        'total_orders': total_orders,
        'months' : months,
        'orders' : orders,
        'users' : users
    } """
    return render(request,"admin/dashboard.html")

@user_is_admin
def product_create(request):
    product_form = ProductForm()
    product_image_form = ProductImageForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST or None, request.FILES or None)
        product_image_form = ProductImageForm(request.POST or None, request.FILES or None)
        images = request.FILES.getlist('image')
        if product_form.is_valid():
            name = product_form.cleaned_data['product_name']
            category = product_form.cleaned_data['category']
            main_image = product_form.cleaned_data['product_image']
            description = product_form.cleaned_data['product_desc']
            price = product_form.cleaned_data['price']
            stock = product_form.cleaned_data['stock']
            is_available = product_form.cleaned_data['is_available']
            product = Product.objects.create(product_name=name, category=category, product_image=main_image, product_desc=description, price=price, is_available=is_available, stock=stock)

            for image in images:
                ProductImage.objects.create(product=product, product_image=image)
            messages.success(request, "Product Created")
            return redirect('product_list')
        else:
            messages.error(request,"Product creation failed ")

    context ={
        'product_form': product_form,
        'product_image_form': product_image_form
    }

    return render(request,"admin/product_create.html", context)

@user_is_admin
def product_update(request, product_id):
    product = Product.objects.get(id = product_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Product Updated Successfully')
            return redirect(to='product_list')
    else:
        product_form = ProductForm(instance=product)
        
    return render(request,"admin_dashboard/product_update.html",  {'product_form': product_form})

@user_is_admin
def product_delete(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        product.delete()
        render(request, 'admin_dashboard/product.html')
    return redirect(to='product_list')

#=====END PRODUCT=====