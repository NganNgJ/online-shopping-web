from rest_framework import routers
from django.urls import path, re_path, include
from .views import (
    ProductCategoryViewset,
    ProductViewset,
    UserAddressViewset
)


router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewset)
router.register(r'product', ProductViewset)
router.register(r'profile/address', ProductViewset)


urlpatterns = [
    path('', include(router.urls)),
]
