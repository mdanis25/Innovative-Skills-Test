# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, VerifyEmailAPIView, ProductListAPIView

router = DefaultRouter()
router.register('register', UserViewSet, basename='register') 
router.register('products', ProductListAPIView, basename='products')

urlpatterns = [
    path('', include(router.urls)), 
    path('verify_email/<str:username>/', VerifyEmailAPIView.as_view(), name='verify_email')
]
