from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = [
            'name', 
            'description',
            'price'
        ]


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = [
            'firstname',
            'lastname',
            'address',
            'city'
        ]

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            'orderdatetime',
            'paymentmode',
            'quantity',
            'food',
            'customer'
        ]

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]