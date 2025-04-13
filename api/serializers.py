# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import OtpToken 

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer): 
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 6},
            'confirm_password': {'write_only': True}
        } 
        
    def create(self, validated_data):
        validated_data.pop('confirm_password', None) 
        user = User.objects.create_user(**validated_data)
        return user
        

class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)
