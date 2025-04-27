
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone 
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models import OtpToken  
from products.models import Product 
from purchase.models import Purchase 
from rest_framework import generics
from installments.models import Installment
from .serializers import InstallmentSerializer
from api.serializers import UserRegisterSerializer, EmailVerifySerializer, ProductSerializer, PurchaseSerializer, InstallmentSerializer 
from installments.task import send_due_installment_reminders

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def get_queryset(self):
        return self.queryset.filter(is_superuser=False)

    def create(self, request, *args, **kwargs):
        """Override to simplify response"""
        return super().create(request, *args, **kwargs)



class VerifyEmailAPIView(APIView):
    def post(self, request, username):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']

        try:
            user = User.objects.get(email=email)
            otp = user.otps.latest('otp_created_at')

            if otp.otp_code == otp_code and otp.otp_expires_at > timezone.now():
                user.is_active = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        except (User.DoesNotExist, OtpToken.DoesNotExist):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
 
 
# ============================================================
#                     # Product Viewset
# ============================================================ 
class ProductListAPIView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    permission_classes = [IsAuthenticated] 
    

# ============================================================          
#                     # Purchase Viewset
# ============================================================
class PurchaseListAPIView(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated] 
    
     
class InstallmentCreateAPIView(generics.CreateAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer

    def perform_create(self, serializer):
        installment = serializer.save()

        # If this is the first paid installment
        purchase = installment.purchase
        paid_installments = purchase.installments.filter(status='paid')

        if paid_installments.count() == 1:
            # Create 2nd installment (pending) after 30 days
            second_due_date = installment.payment_date + timedelta(days=30)
            Installment.objects.create(
                purchase=purchase,
                paid_amount=purchase.total_price - installment.paid_amount,
                due_date=second_due_date,
                status='pending'
            )

            # Schedule reminder 5 days before second_due_date
            reminder_eta = second_due_date - timedelta(days=5)
            delay_seconds = (reminder_eta - timezone.now()).total_seconds()

            if delay_seconds > 0:
              send_due_installment_reminders.apply_async(
                    kwargs={'purchase_id': purchase.purchase_id},
                    countdown=delay_seconds
                )

class InstallmentListAPIView(generics.ListAPIView):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(purchase__user=user)
 