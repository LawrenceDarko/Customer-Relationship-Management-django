from re import template
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from accounts.models import *
from .forms import OrderForm

# Create your views here.

def home(request):
    orders = Order.objects.all().order_by('-date_created')
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    total_deliveries = orders.filter(status="Delivered").count()
    total_pendings = orders.filter(status="Pending").count()
    
    context = {"orders":orders, "customers":customers, "total_customers":total_customers, "total_orders":total_orders, "total_deliveries":total_deliveries, "total_pendings":total_pendings}
    template = "accounts/dashboard.html"
    return render(request, template, context)


def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    # order_set is a child class while Customer is parent class therefore it prints all the queryset of order under a particular customer
    orders = customers.order_set.all()
    total_orders = orders.count()
    context = {"customers":customers, "orders":orders, "total_orders":total_orders}
    template = "accounts/customers.html"
    return render(request, template, context)


def products(request):
    products = Product.objects.all()
    context = {"products":products}
    template = "accounts/products.html"
    return render(request, template, context)


def create_order(request):
    form = OrderForm()
    if request.method == 'POST':
        # print(request.POST) #request.POST holds the information we selected or posted
        form = OrderForm(request.POST) #This means fix the information we've selected into the form frame OrderForm
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    template = "accounts/order_form.html"
    return render(request, template, context)

def create_order_customer(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=6)
    customer = Customer.objects.get(id=pk) 
    # form = OrderForm(initial={'customer':customer})
    form = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        form = OrderFormSet(request.POST, instance=customer) #This means fix the information we've selected into the form frame OrderForm
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    template = "accounts/order_form_customer.html"
    return render(request, template, context)


def update_order(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) #This helps to fill the fields with an instance of the item clicked
    if request.method == 'POST': 
        form = OrderForm(request.POST, instance=order) #The instance=order is to make sure we don't create new item but rather edit the instance selected by the above code
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    template = "accounts/order_form.html"
    return render(request, template, context)

def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST': 
        order.delete()
        return redirect('/')

    context = {"item":order}
    template = "accounts/delete.html"
    return render(request, template, context)