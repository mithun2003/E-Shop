from django import forms
from .models import  *
from django.forms import ClearableFileInput
from account.models import User
import datetime

   
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            message = "Password doesn't match!"
            self.add_error('confirm_password', message)

    def _init_(self, *args, **kwargs):
        super(UserForm, self)._init_(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'

class CategoryForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}),required=False)

    class Meta:
        model = Category
        fields = ['category_name','cat_slug']
    
class ProductForm(forms.ModelForm):
    slug = forms.SlugField(widget=forms.TextInput(attrs={'class': 'form-input'}),required=False)
    main_image = forms.FileField()

    class Meta:
        model = Product
        fields = ['product_name','category','slug','product_image','product_desc','stock','price','is_available']
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['product_image']
        widgets = {
            'product_image': ClearableFileInput(attrs={'multiple': True}),
        }
