
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.contrib.auth import get_user_model
from accounts.models import OtpToken
from api.serializers import UserRegisterSerializer, EmailVerifySerializer

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
