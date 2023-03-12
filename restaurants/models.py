from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    open = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.restaurant_name}"


class Burger(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='', unique=True)
    description = models.CharField(max_length=300, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=3)
    vegetarian = models.BooleanField(default=False)

    def __str__(self):
        return self.name



