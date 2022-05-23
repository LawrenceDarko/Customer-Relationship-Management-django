from re import template
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from accounts.models import *
from .forms import OrderForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.
@login_required(login_url='/login')
# @allowed_users(allowed_roles=['admin'])
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

@login_required(login_url='/login')
def customers(request, pk):
    customers = Customer.objects.get(id=pk)
    # order_set is a child class while Customer is parent class therefore it prints all the queryset of order under a particular customer
    orders = customers.order_set.all() #This means return all the orders under the particular customer
    total_orders = orders.count()
    context = {"customers":customers, "orders":orders, "total_orders":total_orders}
    template = "accounts/customers.html"
    return render(request, template, context)

@login_required(login_url='/login')
def products(request):
    products = Product.objects.all()
    context = {"products":products}
    template = "accounts/products.html"
    return render(request, template, context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def create_order_customer(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=6)
    customer = Customer.objects.get(id=pk) 
    # form = OrderForm(initial={'customer':customer})
    form = OrderFormSet(queryset=Order.objects.none(), instance=customer) #queryset=Order.objects.none() delete any order instance from the form
    if request.method == 'POST':
        form = OrderFormSet(request.POST, instance=customer) #This means fix the information we've selected into the form frame OrderForm
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {"form":form}
    template = "accounts/order_form_customer.html"
    return render(request, template, context)

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST': 
        order.delete()
        return redirect('/')

    context = {"item":order}
    template = "accounts/delete.html"
    return render(request, template, context)

@unauthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            username = form.cleaned_data.get('username') #Get the username
            messages.success(request, 'Account was created for '+ username) #Display flash message
            return redirect('/login')
    context = {"form":form}
    template = "accounts/registration/register.html"
    return render(request, template, context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        messages.error(request, 'Check username or password')
        if user is not None:
            login(request, user)
            return redirect('accounts:dashboard')

    # context = {"user":user}
    template = "accounts/registration/login.html"
    return render(request, template)

def logout_user(request):
    logout(request)
    return redirect('/login')


def user_page(request):
    context = {}
    template = "accounts/user.html"
    return render(request, template, context)