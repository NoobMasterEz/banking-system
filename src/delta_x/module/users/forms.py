from django.forms import ModelForm
from .models import Customer, User


class CustomerCreationForm(ModelForm):

    class Meta:
        model = Customer
        fields = ('user',)


class CustomerChangeForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'


class UserChangeForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)
