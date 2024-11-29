from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('cartitems', CartItemModelViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('sign_in', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign_in/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign_up', sign_up, name='sign_up'),
    path('update_profie', update_user_profile, name='update_user_profile'),
    path('change_username/<str:username>', ChangeUsername.as_view(), name='change_username'),
    path('change_role/<str:username>', ChangeRole.as_view(), name='change_role'),
    path('change_password:<str:username>', change_password_admin, name='change_password_admin'),
    path('change_password', change_password, name='change_password'),
    path('admin/read_category', read_catgory, name='read_category'),
    path('admin/create_category', create_category, name='create_category'),
    path('admin/update_category/<int:category_id>', update_category, name='update_category'),
    path('admin/delete_category/<int:category_id>', delete_category, name='delete_category'),
    path('admin/read_product', ReadProduct.as_view(), name='read_product'),
    path('admin/create_product', CreateProduct.as_view(), name='create_product'),
    path('admin/update_product/<int:pk>', UpdateProduct.as_view(), name='update_product'),
    path('admin/delete_product/<int:pk>', DeleteProduct.as_view(), name='delete_product'),
    path('admin/read_product/<int:pk>', ReadProductDetail.as_view(), name='read_product_detail'),
    path('admin/read_product_category/<str:category_name>', read_product_category, name='read_product_category'),
    path('shop', shop, name='shop'),
    path('product/<int:product_id>', product_detail, name='product_detail'),
    path('category/<str:category_name>', CategoryProduct.as_view(), name='category'),


]