from django.urls import path
from . import views

app_name = 'webkiosk'
urlpatterns = [
    path('', views.index),
    path('user/', views.userpage, name='user-page'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('food/', views.listfood, name='food-list'),
    path('food/new/', views.createfood, name='food-create'),
    path('food/<int:pk>/', views.detailfood, name='food-detail'),
    path('food/<int:pk>/edit/', views.updatefood, name='food-update'),
    path('food/<int:pk>/delete', views.deletefood, name='food-delete'),
    path('customer/', views.listcustomer, name='customer-list'),
    path('customer/<int:pk>/', views.detailcustomer, name='customer-detail'),
    path('customer/<int:pk>/edit/', views.updatecustomer, name='customer-update'),
    path('customer/<int:pk>/edits/', views.updateCustomer, name='customer-updates'),
    path('customer/new/', views.createcustomer, name='customer-create'),
    path('customer/<int:pk>/delete', views.deletecustomer, name='customer-delete'),
    path('customer/<str:pk>ss/', views.customerprofile, name='customer_profile'),
    path('order/', views.listorder, name='order-list'),
    path('order/new/', views.createorder, name='order-create'),
    path('order/<int:pk>/edit/', views.updateorder, name='order-update'),
    path('order/<int:pk>/', views.detailorder, name='order-detail'),
    path('order/<int:pk>/delete', views.deleteorder, name='order-delete'),
    path('profile/', views.adminuser, name='admin-detail')
]