from rest_framework import routers
from django.urls import path, re_path, include


router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
]
