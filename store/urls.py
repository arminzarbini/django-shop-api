from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/sign_in', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/sign_in/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sign_up', sign_up, name='sign_up'),
    path('api/show_products', show_products, name='show_products'),
    path('api/admin/read_category', read_catgory, name='read_category'),
    path('api/admin/create_category', create_category, name='create_category'),
    path('api/admin/update_category:<int:category_id>', update_category, name='update_category'),
    path('api/admin/delete_category:<int:category_id>', delete_category, name='delete_category'),

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)