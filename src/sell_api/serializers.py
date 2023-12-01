
from rest_framework import serializers
from rest_framework.response import Response
from .models import (
    Users,
    ProductCategory,
    Product,
    Address
)


class RegistrationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(max_length=50, min_length=6)
    phone = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = Users
        fields = ('email', 'phone' , 'password')
    
    def validate(self, args):
        email = args.get('email', None)
        phone = args.get('phone', None)
        if Users.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('Email already exists')})
        if Users.objects.filter(phone=phone).exists():
            raise serializers.ValidationError({'phone':('Phone number already exists')})
        return super().validate(args)        

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)

class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Address
        fields = '__all__'

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        return product
    
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance