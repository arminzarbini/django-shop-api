from django.shortcuts import render
from .models import *
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class ShopPagination(PageNumberPagination):
    page_size = 3


@api_view(['POST']) #check
@permission_classes([AllowAny])
def sign_up(request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.create(validated_data=request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT']) #check
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    data = request.data
    user = request.user
    serializer = UserProfileUpdateSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUserProfieAdmin(APIView): #check
    permission_classes = ([IsAdminUser])
    def put(self, request, username):
        data = request.data
        try:
            user = User.objects.get(username=username)
            serializer = UserProfileUpdateSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'name':['This username does not exist']}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT']) #check
@permission_classes([IsAuthenticated])
def change_username(request):
    data = request.data
    user = request.user
    serializer = ChangeUsernameSerializer(user, data=data)
    if serializer.is_valid():
        serializer.update(instance=user, validated_data=data)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUsernameAdmin(APIView): #check
    permission_classes = ([IsAdminUser])
    def put(self, request, username):
        data = request.data
        try:
            user = User.objects.get(username=username)
            serializer = ChangeUsernameSerializer(user, data=data)
            if serializer.is_valid():
                serializer.update(instance=user, validated_data=data)
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"username":["This username dose not exist"]}, status=status.HTTP_404_NOT_FOUND)


class ChangeRole(APIView): #check
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
            return Response({"username":["This username dose not exist"]}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT']) #check
@permission_classes([IsAdminUser])
def change_password_admin(request, username):
    data = request.data
    try:
        user = User.objects.get(username=username)
        serializer = ChangePasswordSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'password changed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({"username":["This username dose not exist"]}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT']) #check
@permission_classes([IsAuthenticated])
def change_password(request):
    data = request.data
    user = request.user
    serializer = ChangePasswordSerializer(user, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'password changed'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET']) #check
@permission_classes([IsAdminUser])
def read_catgory(request):
    categories = Category.objects.all().order_by('created_at').reverse()
    serializer = CategorySerializer(categories, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST']) #check
@permission_classes([IsAdminUser])
def create_category(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(data=serializer._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT']) #check
@permission_classes([IsAdminUser])
def update_category(request, category_id):
    data = request.data
    try:
        category = Category.objects.get(id=category_id)
    except:
        return Response({"name":["This category id does not exist"]}, status=status.HTTP_404_NOT_FOUND)
    else:
        serializer = CategorySerializer(category, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE']) #check
@permission_classes([IsAdminUser])
def delete_category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except:
        return Response({"name":["This category id does not exist"]}, status=status.HTTP_404_NOT_FOUND)
    else:
        Category.objects.filter(id=category_id).delete()
        return Response({'message':'category deleted'}, status=status.HTTP_204_NO_CONTENT)


class ReadProduct(generics.ListAPIView): #check
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class CreateProduct(APIView): #check
    permission_classes = [IsAdminUser]
    def post(self, request):
        if request.data.get('category'):
            category_name = request.data['category']
            category = Category.objects.get(name=category_name)
            request.data['category'] = category.id
            data = request.data
            serializer = CreateUpdateProductSerializer(data=data)
        else:
            data = request.data
            serializer = CreateUpdateProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProduct(generics.UpdateAPIView): #check
    queryset = Product.objects.all()
    serializer_class = CreateUpdateProductSerializer
    permission_classes = [IsAdminUser]
    

class DeleteProduct(generics.DestroyAPIView): #check
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ReadProductDetail(generics.RetrieveAPIView): #check
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET']) #check
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
    

@api_view(['GET']) #check
@permission_classes([AllowAny])
def shop(request):
    products = Product.objects.all().order_by('created_at').reverse()
    paginator = ShopPagination()
    paginated_products = paginator.paginate_queryset(products, request)
    serializer = ShopSerializer(paginated_products, many=True)
    return paginator.get_paginated_response(data=serializer.data)


@api_view(['GET']) #check
@permission_classes([AllowAny])
def product_detail(request, product_id):
    if Product.objects.filter(id=product_id).exists():
        product = Product.objects.get(id=product_id)
        serializer = ProductDetailSerializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error':'This product id does not exist'}, status=status.HTTP_404_NOT_FOUND)
    

class CategoryProduct(APIView): #check
    permission_classes = ([AllowAny])
    def get(self, request, category_name):
        if Category.objects.filter(name=category_name).exists():
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category).order_by('created_at').reverse()
            paginator = ShopPagination()
            paginated_products = paginator.paginate_queryset(products, request)
            serializer = ShopSerializer(paginated_products, many=True)
            return paginator.get_paginated_response(data=serializer.data)
        else:
            return Response({'error':'This category does not exist'}, status=status.HTTP_404_NOT_FOUND)
        

class AllOrder(generics.ListAPIView): #check
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff == True and user.is_superuser == True:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=user)
        

@api_view(['GET']) #check
@permission_classes([IsAuthenticated])
def checkout_cart(request):
    cart_id = request.data.get('cart_id')
    cart = Cart.objects.get(id=cart_id)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status.HTTP_200_OK)
                            

@api_view(['GET']) #check
@permission_classes([IsAuthenticated])
def checkout_address(request):
    user = request.user
    address = Address.objects.filter(user=user)
    serializer = AddressSerializer(address, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class RecordOrder(generics.CreateAPIView): #check
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = RecordOrderSerializer

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class AllOrderUser(APIView): #check
    parser_classes = [IsAdminUser]
    def get(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            orders = Order.objects.filter(user=user)
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error':'This Username does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT']) #check
@permission_classes([IsAdminUser])
def change_order_status(request, order_code):
    data = request.data
    try:
        order = Order.objects.get(code=order_code)
        serializer = ChangeOrderStatusSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'error':'this order code does not exist'}, status=status.HTTP_404_NOT_FOUND)

    

class AddressUser(APIView): #check
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        address = Address.objects.filter(user=user)
        serializer = AddressSerializer(address, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        user = request.user
        request.data['user'] = user.id
        data = request.data
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, address_id):
        user = request.user
        request.data['user'] = user.id
        data = request.data
        try:
            address = Address.objects.get(id=address_id, user=user)
            serializer = AddressSerializer(address, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, address_id):
        user = request.user
        try:
            address = Address.objects.get(id=address_id, user=user)
            address.delete()
            return Response({'message':'address deleted'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)


class AddressUserAdmin(APIView): #check
    permission_classes = [IsAdminUser]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            address = Address.objects.filter(user=user)
            serializer = AddressSerializer(address, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'error':'This username does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
            request.data['user'] = user.id
            data = request.data
            serializer = AddressSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)            
            else:
                return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'This username does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, username, address_id):
        try:
            user = User.objects.get(username=username)
            request.data['user'] = user.id
            data = request.data
            try:
                address = Address.objects.get(id=address_id, user=user)
                serializer = AddressSerializer(address, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'This username does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, username, address_id):
        try:
            user = User.objects.get(username=username)
            try:
                address = Address.objects.get(id=address_id, user=user)
                address.delete()
                return Response({'message':'address deleted'}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':'This username does not exist'}, status=status.HTTP_404_NOT_FOUND)


class CartItemModelViewSet(ModelViewSet): #check
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        try:
            product_id = request.data.get('product_id')
            product = Product.objects.get(id=product_id)
            quantity = int(request.data.get('quantity'))
            session_key = request.session.session_key
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            if Cart.objects.filter(session_key=session_key).exists():
                cart = Cart.objects.get(session_key=session_key)
                if CartItem.objects.filter(product_id=product_id, cart=cart).exists():
                    return Response({'message':'This product is in the shopping cart'})
            if quantity < 1:
                return Response({'error':'Quantity is less than one'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            elif quantity > product.inventory:
                return Response({'error':'Inventory is less than order quantity', 'inventory':product.inventory}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            else:
                if Cart.objects.filter(session_key=session_key).exists():
                    cart = Cart.objects.get(session_key=session_key)
                    cartitem = CartItem.objects.create(product_id=product_id, cart=cart, quantity=quantity)
                    serializer = CartItemSerializer(cartitem)
                    return Response({'data': serializer.data, 'message': 'item created'}, status=status.HTTP_201_CREATED)
                else:
                    cart = Cart.objects.create(session_key=session_key)
                    cartitem = CartItem.objects.create(product_id=product_id, cart=cart, quantity=quantity)
                    serializer = CartItemSerializer(cartitem)
                    return Response({'data': serializer.data, 'message': 'item created'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['PUT'])
    def update_item(self, request, pk):
        try:
            cartitem = CartItem.objects.get(id=pk)
            inventory = cartitem.product.inventory
            quantity = int(request.data.get('quantity'))
            if quantity < 1:
                cartitem.delete()
                return Response({'message':'item deleted'}, status=status.HTTP_204_NO_CONTENT)
            else:
                if quantity > inventory:
                    return Response({'error':'Inventory is less than order quantity', 'inventory':inventory}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                else:
                    cartitem.quantity = quantity
                    cartitem.save()
                    serializer = CartItemSerializer(cartitem)
                    return Response({'data': serializer.data, 'message': 'item updated'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'There is a problem'}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['GET'])
    def cartitem_quantity(self, request):
        product_id = request.query_params.get('product_id')
        cart_id = request.query_params.get('cart_id')
        try:
            cartitem = CartItem.objects.get(product_id=product_id, cart_id=cart_id)
            quantity = cartitem.quantity
            return Response(quantity)
        except:
            quantity = 0
            return Response(quantity)