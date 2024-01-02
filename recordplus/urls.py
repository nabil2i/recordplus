"""
URL configuration for recordplus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Record Plus API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.recordplus.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="Test License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# api version prefix
api_version = 'v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    ## allauth authentication
    # path('accounts/', include('allauth.urls')),
    
    ## djoser authentication
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    ## standard authentication
    # path('api/auth/', include('core.urls')),
    # path(f'api/social_auth/', include(('social_auth.urls', 'social_auth'), namespace="social-auth")),
    
    ## record api
    path(f'api/{api_version}/record/', include('record.urls')),
    
    ## swagger
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path(f'api/{api_version}/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'api/{api_version}/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'api/{api_version}/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path(f'api/{api_version}/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

## for frontend urls
# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='home.html'))]
