from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator, int_list_validator

import string
import random

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, validators=[int_list_validator(sep=''), MinLengthValidator(11)], null=True, blank=True)
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
    role = models.CharField(max_length=8, choices=RoleChoices, default=RoleChoices.CUSTOMER)

    def __str__(self):
        return f'{self.id}:{self.username}'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    state = models.CharField(max_length=100, default='tehran')
    city = models.CharField(max_length=100, default='tehran')
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10, validators=[int_list_validator(sep=''), MinLengthValidator(10)], null=True, blank=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=11, validators=[int_list_validator(sep=''), MinLengthValidator(11)], default='09352993173')

    def __str__(self):
        return f'{self.id}'

class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.id}:{self.name}'
    
    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def get_default_category():
        return Category.objects.get_or_create(name='uncategorized')[0].id
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=get_default_category)
    name = models.CharField(max_length=100)
    brand = models.CharField(default='unknown', max_length=30)
    content = models.CharField(max_length=255, null=True, blank=True)
    banner = models.ImageField(null=True, blank=True, upload_to='images/product/')
    inventory = models.IntegerField(default=0)
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(null=True, blank=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}:{self.name}'
    
    def discount_price(self):
        return (self.price) -  (((self.price) * (self.discount_percentage)) / 100)
    
    def save(self, *args, **kwargs):
        if self.discount_percentage == 0:
            self.discount = False
        else:
            self.discount = True
        super(Product, self).save(*args, **kwargs)
    

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def get_code():
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=int(6)))
            if Order.objects.filter(code=code).exists():
                continue
            else:
                return code
    code = models.CharField(max_length=6, default=get_code)
    total_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    class DeliveryMethodChoices(models.TextChoices):
        SEND = 'SEND', 'Send'
        PLACE = 'PLACE', 'Place'
    delivery_method = models.CharField(max_length=10, choices=DeliveryMethodChoices, default=DeliveryMethodChoices.SEND)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}:{self.code}:{self.user.username}'


class OrderItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='items')
    quantity = models.IntegerField(default=1)
    total_item_price = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.order.code}:{self.product.name}'

class Cart(models.Model):
    session_key = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.id}:{self.session_key}'
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.id}--->{self.product.name}:{self.cart}:{self.quantity}'