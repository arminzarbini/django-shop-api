from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import ShopSerializer, SignUpSerializer, SignInSerializer, CategorySerializer, ProductSerializer
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView



# Create your views here.

@api_view(['get'])
@permission_classes([AllowAny])
def show_products(request):
    products = Product.objects.all().order_by('created_at').reverse()
    product = ShopSerializer(products, many=True)
    return Response(data=product.data, status=status.HTTP_200_OK)


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
    category = Category.objects.get(id=category_id)
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

