from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import CustomerChangeForm, CustomerCreationForm
from .models import Customer, User
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    model = Customer
