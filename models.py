from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id}: {self.firstname} {self.lastname}, {self.address}, {self.city}'


class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.id}: {self.name}, {self.description}, {self.price}'


class Order(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('CH', 'Cash'),
        ('CD', 'Card')
    ]
    # orderdatetime = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    orderdatetime = models.DateTimeField(default=timezone.now)
    paymentmode = models.CharField(max_length=2, choices=PAYMENT_MODE_CHOICES)
    

    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    

    def __str__(self):
        return f'{self.id}: {self.customer.firstname} {self.customer.lastname}, {self.food.name}, {self.quantity}, {self.paymentmode}, {self.orderdatetime}'

    def total_price(self):
        return self.quantity * self.food.price
    



