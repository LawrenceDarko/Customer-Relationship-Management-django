from django import urls
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home),
    path('customers/', views.customers),
    path('products/', views.products)
]
