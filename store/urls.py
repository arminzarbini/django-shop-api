from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/sign_in', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/sign_in/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/show_products', show_products, name='show_products'),
    path('api/sign_up', sign_up, name='sign_up'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)