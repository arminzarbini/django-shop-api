from rest_framework import serializers
from .models import Product, User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'brand', 'banner', 'price', 'discount', 'discount_percentage', 'discount_price']


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), message='This email is already exists')])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match"})

        return attrs
