from django.db import models

from admin_custom.models import Category
""" from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here. """

""" class Category(models.Model):
    category_name= models.CharField(max_length=50,unique=True)
    cat_slug = models.SlugField(max_length=100,unique=True)
       
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'categories'

    def get_url(self):
            return reverse('products_by_category',args=[self.cat_slug])
        
        
    def __str__(self):
        return self.category_name
     """
def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)
"""     
class Product(models.Model):
    product_name = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=200, unique=True)
    product_desc = models.TextField() 
    product_price = models.CharField(max_length=7)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='') 
    product_image = models.ImageField( upload_to='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product_name
    def get_url(self):
        return reverse('product_detail',args=[self.category.cat_slug, self.slug])
         """
        
""" class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)

    def size(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

class Variation(models.Model):
    variation_category_choice=(
        ('color','color'),
        ('size','size'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default='')
    variation_category= models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    
    objects=VariationManager()
    
    def __str__(self):
        return self.variation_value """
    
""" class ProductGallery(models.Model):
    product = models.ForeignKey(Product,default=None,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='product',max_length=255)
    default = models.BooleanField(default=False)
    def __str__(self):
        return self.product.product_name
    
    class Meta:
        verbose_name='productgallery'
        verbose_name_plural = 'product gallery' """
"""         
class Banner(models.Model):
    name = models.CharField(max_length=200) 
    image = models.ImageField(default='' , upload_to='banner')
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
 """
