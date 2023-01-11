from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category) 
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    list_display=['image','product']


class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','slug','category','price','is_available','created_at','updated_at','stock']
    list_filter=['is_available','created_at','updated_at','category']
    list_editable=['is_available']
    prepopulated_fields={'slug':('product_name',)}
    inlines = [ProductImageAdmin]
admin.site.register(Product, ProductAdmin)
 
