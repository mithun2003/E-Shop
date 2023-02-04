from django.db import models
from account.models import *
from admin_custom.models import Product,Variation
# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100,blank=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.FloatField()
    status = models.CharField(max_length=100,default='pending')
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.payment_id
    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Placed', 'Placed'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
        ('Refunded', 'Refunded')
    )
 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # phone_number = models.CharField(max_length=15)
    # email = models.EmailField(max_length=50)
    # address_line_1 = models.CharField(max_length=100)
    # address_line_2 = models.CharField(max_length=100, blank=True)
    # country = models.CharField(max_length=50)
    # state = models.CharField(max_length=50)
    # city = models.CharField(max_length=50)
    # pincode=models.IntegerField()
    address = models.ForeignKey(Address,null=True,on_delete=models.CASCADE)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField(null=True)
    tax = models.FloatField(null=True)
    status = models.CharField(max_length=100, choices=STATUS, default='Pending')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def full_address(self):
        return f'{self.address.address_line_1} {self.address.address_line_2}'
    
    def __str__(self):
        return self.user.first_name

class OrderProduct(models.Model):
  
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()

    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)
    def total_price(self):
        if self.product.is_offer:
            return self.quantity * self.product.offered_price 
        else:  
            return self.quantity * self.product_price
         
    def __str__(self):
        return self.product.product_name
    
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.pk}"