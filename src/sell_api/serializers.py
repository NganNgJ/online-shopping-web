from __future__ import absolute_import, unicode_literals
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .error_codes import ERROR_CODES
from .enum import (OrderStatus, PaymentStatus, PaymentMethod)
from .models import (
    Users,
    ProductCategory,
    Product,
    Address,
    Order,
    OrderItem,
    Payment
)
from . import tasks
from celery.result import AsyncResult


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

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users 
        fields = ['id', 'email', 'phone', 'full_name', 'is_active']

class AddressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Address.objects.create(user=user, **validated_data)

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

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'order_item_price']

class OrderSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    order_items = serializers.ListField(write_only=True, required=True)
    product_list = OrderItemSerializer(many=True, read_only=True, source='order_items')

    class Meta:
        model = Order
        fields = ['id', 'product_list', 'total_price', 'buyer', 'order_items', 'shipping_address', 'is_cart', 'status', 'discount_amount']
    
    def validate(self, validated_data):
        products_data = validated_data.get('order_items', [])
        for product_data in products_data:
            product_id = product_data['product']
            quantity = product_data['quantity']
        
            product = Product.objects.filter(id=product_id, is_active=True).first()

            if product is None:
                return ParseError(ERROR_CODES[400001], 400001)
            if quantity > product.quantity:
                return ParseError(ERROR_CODES[400002], 400002)
        
        return validated_data 

    def create(self,validated_data):
        buyer = self.context['request'].user 
        order_items_data = validated_data.get('order_items', [])
        validated_data.pop('order_items')
        order = Order.objects.create(buyer=buyer, **validated_data)     

        #create Order Item from task
        task = tasks.create_order_item.delay(order_items_data, order.id)
        return order 

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(required=True, allow_null=False, write_only=True)
    payment_method = serializers.CharField(required=True, allow_null=False)
    status = serializers.CharField(required=True, allow_null=False)
    amount = serializers.FloatField(required=True, allow_null=False)
    
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, validated_data):
        order_id = validated_data.get('order_id', None)
        payment_method = validated_data.get('payment_method', None)
        status = validated_data.get('status',None)
        user = self.context['request'].user

        order = Order.objects.filter(id=order_id, buyer=user).first()

        if order is None:
            raise ParseError(ERROR_CODES[400005],400005)
        if payment_method not in [item.value for item in PaymentMethod]:
            raise ParseError(ERROR_CODES[400004],400004)
        if status not in [status.value for status in PaymentStatus]:
            raise ParseError(ERROR_CODES[400007],400007)
        
        return validated_data
    
    def create(self,validated_data): 
        user = self.context['request'].user
        order_id = validated_data.get('order_id', None)
        payment_method = validated_data.get('payment_method', None)
        status = validated_data.get('status',None)
        amount = validated_data.get('amount',None)

        payment = Payment.objects.create(user=user,**validated_data)
        if status == 'Success':
            Order.objects.filter(id=order_id).update(status='Completed')
        
        return payment
    
    def update(self, instance, validated_data):
        status = validated_data.get('status',None)

        if instance.status == 'Success':
            raise ParseError(ERROR_CODES[400006],400006)
        instance.status = status 
        instance.save()
        return instance



     