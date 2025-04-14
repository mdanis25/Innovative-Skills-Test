# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import OtpToken  
from products.models import Product

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
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

class EmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)



# ============================================================ 
                    # Product Serializer
# ============================================================ 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at'] 
        
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be a positive number.")
            return value
        
        def validate_stock(self, value):
            if value < 0:
                raise serializers.ValidationError("Stock cannot be negative.")
            return value
        def validate_name(self, value):
            if not value:
                raise serializers.ValidationError("Name cannot be empty.")
            return value