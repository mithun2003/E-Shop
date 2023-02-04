from django.contrib import admin
from .models import *

# Register your models here.
 
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    list_display=['image','product']


class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_name','slug','category','price','is_available','created_at','updated_at','stock']
    list_display_links=['id','product_name','slug','category']
    list_filter=['is_available','created_at','updated_at','category']
    list_editable=['is_available']
    prepopulated_fields={'slug':('product_name',)}
    inlines = [ProductImageAdmin]
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug':('category_name',)}
    list_display=('category_name','cat_slug')
class VariationAdmin(admin.ModelAdmin):
    list_display=('variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter = ('variation_category','variation_value')
admin.site.register(Variation,VariationAdmin) 
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner)

