# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewSet, VerifyEmailAPIView

router = DefaultRouter()
router.register(r'register', UserViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)), 
    path('verify_email/<str:username>/', VerifyEmailAPIView.as_view(), name='verify_email')
]
