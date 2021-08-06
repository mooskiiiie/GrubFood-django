from .decorators import unauthenticated_user, allowed_users, admin_only
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group




# Create your views here.
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()
    customer = request.user.customer
    print('ORDERS:', orders)
    context = {'orders': orders, 'customer':customer}
    return render(request, 'webkiosk/user.html', context)


@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
        
            Customer.objects.create(user=user,firstname=username, lastname="none", address="none", city="none")
            messages.success(request, 'Account was created for ' + username)
            return redirect('webkiosk:login')

    context = {'form': form}
    return render(request, 'webkiosk/register.html', context )


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('webkiosk:food-list')
        else:
             messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'webkiosk/login.html', context )


def logoutUser(request):
    logout(request)
    return redirect('webkiosk:login')


@login_required(login_url='webkiosk:login')
def index(request): #landing page
    return render(request, 'webkiosk/base.html')


@login_required(login_url='webkiosk:login')
def listfood(request): #list of food
    context = {
        'foodlist': Food.objects.all(),
        'testitem': 'table'
    }
    return render(request, 'webkiosk/food.html', context)


@login_required(login_url='webkiosk:login')
def createfood(request): #create new food item
    if request.method == 'GET':
        form = FoodForm()
    elif request.method == 'POST':
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:food-list')
    
    context = {'form': form}
    return render(request, 'webkiosk/food_form.html', context) 


@login_required(login_url='webkiosk:login')
def detailfood(request, pk): #view food details
    food = Food.objects.get(id=pk)
    context = {'food':food}
    return render(request, 'webkiosk/food_detail.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updatefood(request, pk): #edit food details
    food = Food.objects.get(id=pk)
    if request.method == 'GET':
        form = FoodForm(instance=food)
    elif request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food record successfully updated.')
    
    context = {'form': form}
    return render(request, 'webkiosk/food_form.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deletefood(request, pk): #delete food item
    food = Food.objects.get(id=pk)
    if request.method == 'GET':
        context = {'food': food}
        return render(request, 'webkiosk/food_delete.html', context)
    elif request.method == 'POST':
        food.delete()
        return redirect('webkiosk:food-list')
    

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def listcustomer(request): #list of customers
    context = {
        'customerlist': Customer.objects.all(),
    }
    return render(request, 'webkiosk/customer.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def detailcustomer(request, pk): #customer details
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    context = {'customer':customer, 'orders':orders}

    return render(request, 'webkiosk/customer_detail.html', context)


def customerprofile(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    context = {'orders':orders, 'customer':customer}

    return render(request, 'webkiosk/customer_profile.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updatecustomer(request, pk): #update customer details
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
    elif request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer record successfully updated.')
    
    context = {'form': form}
    return render(request, 'webkiosk/customer_form.html', context)

#regular customers only
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def updateCustomer(request, pk): #update customer details
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
    elif request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer record successfully updated.')
    
    context = {'form': form}
    return render(request, 'webkiosk/customer_form.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def createcustomer(request): #create new customer
    if request.method == 'GET':
        form = CustomerForm()
    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:customer-list')
    
    context = {'form': form}
    return render(request, 'webkiosk/customer_form.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deletecustomer(request, pk): #delete customer
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        context = {'customer': customer}
        return render(request, 'webkiosk/customer_delete.html', context)
    elif request.method == 'POST':
        customer.delete()
        return redirect('webkiosk:customer-list')


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def listorder(request): #list of orders
    context = {
        'orderlist': Order.objects.all(),
        
    }
    return render(request, 'webkiosk/order.html', context)


@login_required(login_url='webkiosk:login')
def createorder(request): #create new order 
    if request.method == 'GET':
        form = OrderForm()
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            group = Group.objects.get(name='customer')
            if group == 'admin':
                return redirect('webkiosk:order-list')
            else:
                return redirect('webkiosk:user-page')
    
    context = {'form': form}
    return render(request, 'webkiosk/order_form.html', context)



@login_required(login_url='webkiosk:login')
def updateorder(request, pk): #update order details
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderForm(instance=order)
    elif request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order record successfully updated.')
            
    
    context = {'form': form}
    return render(request, 'webkiosk/order_form.html', context)


@login_required(login_url='webkiosk:login')
def detailorder(request, pk): #view order details
    order = Order.objects.get(id=pk)
    context = {'order':order}

    return render(request, 'webkiosk/order_detail.html', context)


@login_required(login_url='webkiosk:login')
def deleteorder(request, pk): #delete order
    order = Order.objects.get(id=pk)

    if request.method == 'GET':
        context = {'order': order}
        return render(request, 'webkiosk/order_delete.html', context)
    elif request.method == 'POST':
        order.delete()
        group = Group.objects.get(name='customer')
        if group == 'admin':
            return redirect('webkiosk:order-list')
        else:
            return redirect('webkiosk:user-page')
     

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def adminuser(request):
    context = {}
    return render(request, 'webkiosk/profile.html', context)