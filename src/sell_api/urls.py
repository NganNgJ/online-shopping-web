from rest_framework import routers
from django.urls import path, re_path, include
from .views import (
    ProductCategoryViewset,
    ProductViewset,
    AddressViewset,
    UserViewset,
    OrderViewset,
    PaymentViewset,
    health_check
)


router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewset)
router.register(r'product', ProductViewset)
router.register(r'address', AddressViewset)
router.register(r'user', UserViewset)
router.register(r'order', OrderViewset)
router.register(r'payment', PaymentViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('health_check', health_check)
]
