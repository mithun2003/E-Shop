from django.urls import path
from . import views
urlpatterns = [
    #path('login',views.loginPage,name='login'),  
    path('',views.index,name='home'),
    #path('register',views.registerPage,name='register'),  
    #path('logout',views.logoutUser,name='logout'),  
    path('store',views.store,name='store'),
    path('store/<slug:category_slug>',views.store,name='products_by_category'),
    path('store/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('store/search/',views.search,name='search'),
   
]