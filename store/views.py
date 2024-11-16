from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProductSerializer


# Create your views here.

@api_view(['get'])
def show_products(request):
    products = Product.objects.all().order_by('created_at').reverse()
    product = ProductSerializer(products, many=True)
    return Response(data=product.data, status=status.HTTP_200_OK)