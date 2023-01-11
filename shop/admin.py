from django.contrib import admin
from .models import *
import admin_thumbnails
# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    
class Display(admin.ModelAdmin):
    list_display =('id','product_name','product_price','category','stock','updated_at','created_at')
    prepopulated_fields= {'slug':('product_name',)}
    list_display_links =('id','product_name',)
    filter_horizontal = ()
    
class CustomerDisplay(admin.ModelAdmin):
    list_display =('id','username','email','created_date')
    list_display_links =('id','username',)
    filter_horizontal = ()
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'cat_slug':('category_name',)}
    list_display=('category_name','cat_slug')
class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter = ('product','variation_category','variation_value')
    
   
admin.site.register(Category,CategoryAdmin)
admin.site.register(Variation,VariationAdmin)   
admin.site.register(Product, Display)
admin.site.register(Banner)

admin.site.register(ProductGallery)