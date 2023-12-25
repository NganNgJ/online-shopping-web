from django.shortcuts import render
from rest_framework import generics,status,serializers, viewsets, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from .models import (
    ProductCategory, Product, Address, Users, Order, Payment
)
from .serializers import(
    RegistrationSerializer,
    ProductCategorySerializer,
    ProductSerializer,
    AddressSerializer,
    UserSerializer,
    OrderSerializer,
    PaymentSerializer
)


class RegistrationAPIview(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class= RegistrationSerializer

    def post(self,request):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return Response({'detail': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class ProductCategoryViewset(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AddressViewset(viewsets.ModelViewSet):
    queryset = Address.objects.all() 
    serializer_class = AddressSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

