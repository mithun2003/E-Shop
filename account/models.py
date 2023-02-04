from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils import timezone
#from django.utils import timezone

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self ,first_name, last_name, email, username, phone_number, password=None):
        if not email:
            raise ValueError("User must have a email")
        if not phone_number:
            raise ValueError("User must have a phone number")


        user = self.model(
            email = self.normalize_email(email),
            username  = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )

        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self ,first_name, last_name,phone_number, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username  = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_verified = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length = 50, blank=True)
    last_name = models.CharField(max_length = 50, blank=True)
    username = models.CharField(max_length = 50, unique = True, blank=True)
    email  = models.EmailField(max_length = 100, unique = True,blank=False)
    phone_number = models.CharField(max_length = 10,unique = True)
    date_joined = models.DateField(auto_now_add = True)
    last_login = models.DateField(auto_now_add=True)
    
    is_block = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
      return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
class Address(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE) #we want to have only one profile for one person
    address_line_1  = models.CharField(blank=True, max_length=100 )
    address_line_2  = models.CharField(blank=True, max_length=100 )
    city            = models.CharField(blank=True, max_length=20)
    state           = models.CharField(blank=True, max_length=20)
    country         = models.CharField(blank=True, max_length=20)
    pincode         = models.IntegerField(blank=True,default=None,null=True)
    def __str__(self):
        return self.user.first_name
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    

class OTP(models.Model):
    otp = models.CharField(max_length=6)
    expiration_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)