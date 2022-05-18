from itertools import product
from operator import mod
from sre_constants import CATEGORY
from unicodedata import category, name
from django.db import models

from accounts.views import customers

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)  #null true is telling django if any of these field is empty don't give an error
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True) 

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True) 

    def __str__(self):
        return self.name

class Product(models.Model):

    CATEGORY = (
        ("Indoor", "Indoor"),
        ("Outdoor", "Outdoor")
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag) 

    def __str__(self):
        return self.name




class Order(models.Model):

    STATUS = (
        ("Pending", "Pending"),
        ("Out for delivery", "Out for delivery"),
        ("Delivered", "Delivered")
    )
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    

    def __str__(self):
        return self.product.name