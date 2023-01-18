from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from .models import User,OTP
# Register your models here.
class AccountAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'phone_number','date_joined','last_login','is_active')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('-date_joined',)
    add_fieldsets = (
        (None, {
            'fields': ('email','phone_number', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'username')
        })
    )

admin.site.register(User, AccountAdmin)
