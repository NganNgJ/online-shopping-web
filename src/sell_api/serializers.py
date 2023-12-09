
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .error_codes import ERROR_CODES
from .models import (
    Users,
    ProductCategory,
    Product,
    Address,
    Order,
    OrderItem
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

        for order_item in order_items_data:
            product_id = order_item['product']
            quantity = order_item['quantity']
            product = Product.objects.get(pk=product_id)
            order_item_price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, order_item_price=order_item_price)
        return order 




     