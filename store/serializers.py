from rest_framework import serializers
from .models import Product, User, Category, Cart, CartItem
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name', 'banner', 'price', 'discount', 'discount_percentage', 'discount_price']


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['category_name', 'name', 'brand', 'content', 'banner', 'price', 'discount', 'discount_percentage', 'discount_price', 'description']


class CartItemSerializer(serializers.ModelSerializer):
    product = ShopSerializer(read_only=True)
    product_id = serializers.IntegerField()
    total_item_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_item_price']

    def get_total_item_price(self, cartitem):
        total_item = cartitem.quantity * cartitem.product.price
        return total_item


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    total_cart_item = serializers.SerializerMethodField()
    cartitem = CartItemSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = ['id', 'session', 'cartitem', 'total_cart_item', 'total_price']

    def get_total_price(self, cart):
        total_price = sum([item.quantity * item.product.pirce for item in cart.cartitems.all()])
        return total_price
    
    def get_total_cart_item(self, cart):
        total_cart_item = sum([item.quantity for item in cart.cartitems.all()])
        return total_cart_item



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


class UserProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']


class ChangeUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']


class ChangeRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['role']


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'password_confirm']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords must match"})

        return attrs
    
    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'The password is incorrect'})
        elif validated_data['old_password'] == validated_data['new_password']:
            raise serializers.ValidationError({'password':'old and new passwords are the same'})
        else:
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance
    


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
    
    name = serializers.CharField(required=True, max_length=100, validators=[UniqueValidator(queryset=Product.objects.all(), message='This Product is already exists')])

    class Meta:
        model = Product
        fields = ['category', 'name', 'brand', 'content', 'banner', 'inventory', 'price', 'discount', 'discount_percentage', 'discount_price', 'description', 'archive']
