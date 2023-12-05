from rest_framework import routers
from django.urls import path, re_path, include
from .views import (
    ProductCategoryViewset,
    ProductViewset,
    AddressViewset,
    UserViewset
)


router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewset)
router.register(r'product', ProductViewset)
router.register(r'address', AddressViewset)
router.register(r'user', UserViewset)


urlpatterns = [
    path('', include(router.urls)),
]
