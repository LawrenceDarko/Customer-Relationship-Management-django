from django import urls
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='dashboard'),
    path('products/', views.products, name='product_list'),
    path('customers/<str:pk>/', views.customers, name='customer_detail'),
    path('creat_order/', views.create_order, name='order_item'),
    path('creat_orders/<str:pk>', views.create_order_customer, name='order_create_customer'),
    path('update_order/<str:pk>', views.update_order, name='order_update'),
    path('delete_order/<str:pk>', views.delete_order, name='order_delete'),
    path('login/', views.login_page, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register, name='register_user'),
    path('user/', views.user_page, name='user_page')

]
