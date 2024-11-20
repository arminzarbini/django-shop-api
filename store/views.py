from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import ProductSerializer, SignUpSerializer, SignInSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView



# Create your views here.

@api_view(['get'])
@permission_classes([AllowAny])
def show_products(request):
    products = Product.objects.all().order_by('created_at').reverse()
    product = ProductSerializer(products, many=True)
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

    