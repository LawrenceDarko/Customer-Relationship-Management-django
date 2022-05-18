from re import template
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    template = "accounts/dashboard.html"
    return render(request, template)

def customers(request):
    template = "accounts/customers.html"
    return render(request, template)

def products(request):
    template = "accounts/products.html"
    return render(request, template)