from dataclasses import field
from pyexpat import model
from tkinter import Widget
from django.forms import ModelForm
from .models import Order
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

        # if you wanna select some field you can do:
        # fields = ['customer', 'product' etc]


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder': 'Username' }),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Email Address'}),
            # 'password1': forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}),
        }