from django.forms import ModelForm
from .models import Customer


class CustomerCreationForm(ModelForm):

    class Meta:
        model = Customer
        fields = ('user',)


class CustomerChangeForm(ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
