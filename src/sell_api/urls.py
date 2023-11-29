from rest_framework import routers
from django.urls import path, re_path, include
from .views import (
    ProductCategoryViewset,
    ProductViewset
)


router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewset)
router.register(r'product', ProductViewset)


urlpatterns = [
    path('', include(router.urls)),
]
