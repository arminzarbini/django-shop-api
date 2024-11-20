from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import ProductSerializer, SignUpSerializer
from rest_framework.permissions import AllowAny


# Create your views here.

@api_view(['get'])
def show_products(request):
    products = Product.objects.all().order_by('created_at').reverse()
    product = ProductSerializer(products, many=True)
    return Response(data=product.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def sign_up(request):
    new_user = SignUpSerializer(data=request.data)
    if new_user.is_valid():
        user = User.objects.create(
            username = new_user.validated_data['username'],
            first_name = new_user.validated_data['first_name'],
            last_name = new_user.validated_data['last_name'],
            email = new_user.validated_data['email']
        )
        user.set_password(new_user.validated_data['password'])
        user.save()
        return Response(new_user.data, status=status.HTTP_201_CREATED)
    else:
        return Response(new_user._errors, status=status.HTTP_400_BAD_REQUEST)
    
