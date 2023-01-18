from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    category_name= models.CharField(max_length=50,unique=True)
    cat_slug = models.SlugField(max_length=100,unique=True)
    #created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        
    def get_url(self):
            return reverse('products_by_category',args=[self.cat_slug])
        
    """  def save(self, *args, **kwargs):
        value = self.category_name
        self.cat_slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs) """
    def __str__(self):
        return self.category_name
    

    
class Product(models.Model):
    product_name = models.CharField(max_length=200) 
    slug = models.SlugField(max_length=200, unique=True)
    product_desc = models.TextField() 
    price=models.FloatField()    
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='',related_name='products') 
    product_image = models.ImageField( upload_to='product')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product_name
    """ def save(self, *args, **kwargs):
        value = self.product_name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs) """

    def get_url(self):
        return reverse('product_detail',args=[self.category.cat_slug, self.slug])
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    product_image = models.ImageField(upload_to='product')
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.product.product_name
    
    
class VariationManager(models.Manager):
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
        return self.variation_value 
    
     
class Banner(models.Model):
    name = models.CharField(max_length=200) 
    image = models.ImageField(default='' , upload_to='banner')
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    
