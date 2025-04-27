# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, VerifyEmailAPIView, ProductListAPIView, PurchaseListAPIView, InstallmentCreateAPIView, InstallmentListAPIView

router = DefaultRouter()
router.register('register', UserViewSet, basename='register') 
router.register('products', ProductListAPIView, basename='products')
router.register('purchase', PurchaseListAPIView, basename='purchase')

urlpatterns = [
    path('', include(router.urls)), 
    path('verify_email/<str:username>/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('installments/', InstallmentCreateAPIView.as_view(), name='installments'), 
    path('installments_list/', InstallmentListAPIView.as_view(), name='installments_list'), 
    
]   

