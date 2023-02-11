from django.db import models
from admin_custom.models import Product,Variation
from account.models import User
# Create your models here.

class Coupon(models.Model):
    code = models.CharField(max_length=50,blank=False)
    is_expired = models.BooleanField(default =False)
    amount = models.FloatField(default=10)
    min_amount = models.FloatField(default=500)
    max_use = models.IntegerField(default=100)
    used =  models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.code)
class UsedCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="used_coupons")
    coupon =  models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True, related_name="used_coupons")
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.username)
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True,null=False)
    #user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    #coupon =  models.ForeignKey(Coupon, on_delete=models.SET_NULL,null = True, blank = True, related_name="carts")
    date_added = models.DateField(auto_now_add=True)
   

    def __str__(self):
        return self.cart_id
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        
class CartItem(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete=models.CASCADE)
    coupon =  models.ForeignKey(Coupon, on_delete=models.SET_NULL,null = True, blank = True, related_name="carts")
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name="items")
    cart =  models.ForeignKey(Cart, on_delete=models.CASCADE,null=True, related_name="items")
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default= True)
    
    def sub_total(self):
        if self.product.is_offer:
            return self.product.offered_price * self.quantity
        elif self.product.category.is_offer:
            return self.product.offered_price * self.quantity
        else:
            return self.product.price * self.quantity
    
    
    def get_cart_total(self):
        #items = self.items.all()
        price = []

        #for cart_item in self.items:
        price.append(self.product.price * self.quantity)

        if self.coupon:
            if self.coupon.min_amount < sum(price):
                return sum(price) - self.coupon.amount
        
        return sum(price)
    def expire(self):
        if self.coupon.used>self.coupon.max_use:
                self.coupon.is_expired=True
                self.coupon.save()
            
    def __unicode__(self):
        return self.product
    
    
