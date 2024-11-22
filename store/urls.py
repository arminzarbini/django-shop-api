from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('sign_in', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('sign_in/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign_up', sign_up, name='sign_up'),
    path('show_products', show_products, name='show_products'),
    path('admin/read_category', read_catgory, name='read_category'),
    path('admin/create_category', create_category, name='create_category'),
    path('admin/update_category:<int:category_id>', update_category, name='update_category'),
    path('admin/delete_category:<int:category_id>', delete_category, name='delete_category'),
    path('admin/read_product', ReadProduct.as_view(), name='read_product'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)