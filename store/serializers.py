from rest_framework import serializers
from .models import Product, User, Category
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ShopSerializer(serializers.ModelSerializer):

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
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class SignInSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(SignInSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30, validators=[UniqueValidator(queryset=Category.objects.all(), message='This category is already exists')])
    

    class Meta:
        model = Category
        fields = ['name']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
    
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    def get_category(self, obj):
        return Category.objects.get(id=obj.category.id).name

    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'content', 'banner', 'inventory', 'price', 'discount', 'discount_percentage', 'description', 'archive']