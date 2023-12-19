from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from sell_api.views import RegistrationAPIview
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sell_api.urls')),
    path('auth/register',RegistrationAPIview.as_view(),name='register,'),
    path('auth/login', TokenObtainPairView.as_view(), name= 'login'),
    path('auth/refresh-token',TokenRefreshView.as_view(), name= 'refreshtoken'),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
#Media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
