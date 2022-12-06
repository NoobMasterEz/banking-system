from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import UserChangeForm, UserCreationForm
from .models import Customer, User
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
