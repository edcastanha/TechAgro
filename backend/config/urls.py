"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='../site/index.html'), name='home'),
    path('v1/api/admin/', admin.site.urls),
    path('v1/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('v1/api/', include('core.urls')),
    path('v1/api/', include('produtores.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('v1/api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('v1/api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
