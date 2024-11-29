from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from .serializers import ShopSerializer, SignUpSerializer, SignInSerializer, CategorySerializer, ProductSerializer, ProductDetailSerializer, CartSerializer, CartItemSerializer, UserProfileUpdateSerializer, ChangeUsernameSerializer, ChangeRoleSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

class SignIn(TokenObtainPairView):
    permission_classes = ([AllowAny])
    def post(self, request):
        serializer = SignInSerializer
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_user_profile(request):
    data = request.data
    user = request.user
    serializer = UserProfileUpdateSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsername(APIView):
    permission_classes = ([IsAdminUser])
    def put(self, request, username):
        data = request.data
        try:
            user = User.objects.get(username=username)
            serializer = ChangeUsernameSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"name":["This username dose not exist"]}, status=status.HTTP_404_NOT_FOUND)


class ChangeRole(APIView):
    permission_classes = ([IsAdminUser])
    def put(self, request, username):
        data = request.data
        role = request.data.get('role')
        try:
            user = User.objects.get(username=username)
            serializer = ChangeRoleSerializer(user, data=data)
            if serializer.is_valid():
                if role == "ADMIN":
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                elif role == "CUSTOMER":
                    user.is_superuser = False
                    user.is_staff = False
                    user.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'role field must be ADMIN or CUSTOMER'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"name":["This username dose not exist"]}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def change_password_admin(request, username):
    data = request.data
    user = User.objects.get(username=username)
    serializer = ChangePasswordSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    data = request.data
    user = request.user
    serializer = ChangePasswordSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def read_catgory(request):
    categories = Category.objects.all().order_by('id')
    serializer = CategorySerializer(categories, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_category(request, category_id):
    data = request.data
    try:
        category = Category.objects.get(id=category_id)
    except:
        return Response({"name":["This category id dose not exist"]}, status=status.HTTP_404_NOT_FOUND)
    else:
        if Category.objects.filter(name=data.get('name')).exists():
            return Response({"name":["This category is already exists"]}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = CategorySerializer()
            if serializer.is_valid:
                serializer.update(instance=category, validated_data=data)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(data=serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_category(request, category_id):
    Category.objects.filter(id=category_id).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ReadProduct(APIView):
    permission_classes = ([IsAdminUser])
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateProduct(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class UpdateProduct(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    

class DeleteProduct(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ReadProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET'])
@permission_classes([IsAdminUser])
def read_product_category(request, category_name):
    try:
        category = Category.objects.get(name=category_name)
    except:
        return Response({"name":["This category dose not exist"]}, status=status.HTTP_404_NOT_FOUND)
    else:
        products = Product.objects.filter(category=category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([AllowAny])
def shop(request):
    products = Product.objects.all().order_by('created_at').reverse()
    serializer = ShopSerializer(products, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_detail(request, product_id):
    if Product.objects.filter(id=product_id).exists():
        product = Product.objects.get(id=product_id)
        serializer = ProductDetailSerializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class CategoryProduct(APIView):
    permission_classes = ([AllowAny])
    def get(self, request, category_name):
        if Category.objects.filter(name=category_name).exists():
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category).order_by('created_at').reverse()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CartItemModelViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        try:
            product_id = request.data.get('product_id')

            session = request.session.session_key

            if not session:
                request.session.save()
                session = request.session.session_key
            cart, created = Cart.objects.get_or_create(session=session)
            cartitem, created = CartItem.objects.get_or_create(product_id=product_id, cart=cart)
            if not created:
                cartitem.quantity += 1
                cartitem.save()
            else:
                cartitem.quantity = 1
                cartitem.save()
            serializer = CartItemSerializer(cartitem)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['PUT'])
    def update_item(self, request, pk):
        try:
            cartitem = self.get_object()
            quantity = int(request.data.get('quantity'))
            if quantity >= 1:
                cartitem.quantity = quantity
                cartitem.save()
                serializer = CartItemSerializer(cartitem)
                return Response(serializer.data)
            else:
                cartitem.delete()
                return Response({'message':'item deleted'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'])
    def cartitem_quantity(self, request):
        product_id = request.query_params.get('product_id')
        cart_id = request.query_params.get('cart_id')
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            quantity = CartItem.quantity
            return Response(quantity)
        except:
            quantity = 0
            return Response(quantity)





    