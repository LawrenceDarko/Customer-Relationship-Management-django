from dataclasses import field
from django.forms import ModelForm
from .models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        # if you wanna select some field you can do:
        # fields = ['customer', 'product' etc]