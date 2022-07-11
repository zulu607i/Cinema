"""cinema URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf.urls.static import static

from api.authentication import BearerAuthentication
from api.views import get_token_base64, change_seat_status
from cinema import settings
from api.urls import router
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
      title="Cinema API",
      default_version='v1',
      description="Cinema API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(BearerAuthentication,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('home/', include('ui.urls')),
    path('auth/', include('users.urls')),
    path('reservations/', include('reservation.urls')),
    path('movies/', include('movies.urls')),
    path('api/', include(router.urls)),
    path('get-token/', get_token_base64),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/change-seats/<str:pk>', change_seat_status)
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
