from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=60, null=True)
    #profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=60, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=60, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=60, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Orders(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    products = models.ForeignKey(Products, null=True, on_delete=models.SET_NULL)
    STATUS = (
        ('pending', 'pending'),
        ('out for delivery', 'out for delivery'),
        ('delivered', 'delivered'),
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    Status = models.CharField(max_length=60, null=True, choices=STATUS)

    def __str__(self):
        return self.products.name
