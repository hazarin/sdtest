"""sdtest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.shortcuts import redirect
from django.urls import path, include, re_path


def root_redirect(request):
    schema_view = 'schema-swagger-ui'
    return redirect(schema_view, permanent=True)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),

    # Для использования базовых шаблонов при генерации email'ов конфирмации
    path('accounts/', include('allauth.urls')),
    re_path(r'^', include('django.contrib.auth.urls')),

    re_path(r'^$', root_redirect),
]
