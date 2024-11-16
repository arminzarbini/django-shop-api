from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    class RoleChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
    role = models.CharField(max_length=8, choices=RoleChoices, default=RoleChoices.CUSTOMER)

    def __str__(self):
        return self.username


class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

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
        return f'{self.name}'
    
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
    code = models.CharField(max_length=6)
    total_amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)
    class DeliveryMethodChoices(models.TextChoices):
        SEND = 'SEND', 'Send'
        PLACE = 'PLACE', 'Place'
    delivery_method = models.CharField(max_length=10, choices=DeliveryMethodChoices, default=DeliveryMethodChoices.SEND)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code}:{self.user.username}'


class OrderItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    total_item = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.order.code}:{self.product.name}'