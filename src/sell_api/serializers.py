
from rest_framework import serializers
from rest_framework.response import Response
from .models import (
    Users
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