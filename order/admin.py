from django.contrib import admin
from .models import Payment,Order,OrderProduct,Refund
# Register your models here.

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    extra = 0
    readonly_fields =('user','product','quantity','product_price','order','variations','payment')

class OrderAdmin(admin.ModelAdmin):
    list_display =['id','order_number','user','payment','status','is_ordered','order_total','created_at']
    list_display_links =['id','order_number']

    list_filter = ['status','is_ordered']
    search_fields = ['order_number']
    list_per_page = 10
    readonly_fields =('user','payment','order_note','ip','order_number','order_total','tax','is_ordered','created_at')

    inlines=[OrderProductInline]
    
class OrderProductAdmin(admin.ModelAdmin):
    list_display =['id','user','product','quantity','product_price','created_at']
    list_display_links =['id','user','product','quantity','product_price','created_at']
    readonly_fields =('user','product','quantity','product_price','order','variations','payment','created_at')
class RefundAdmin(admin.ModelAdmin):
    list_display=['id','user','order']   
    list_display_links=['id','user','order']   
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(Refund,RefundAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)