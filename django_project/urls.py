"""
URL configuration for django_project project.

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
from django.contrib import admin
from app1.views import account
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    # name='login' 用于反向解析，比如在模板中使用 {% url 'login' %}，就会自动解析为 /login/
    path('login/', account.login, name='login'),
    path('login_sms/', account.login_sms, name='login_sms'),
    path('login_sms/send_sms_code/', account.send_sms_code, name='send_sms_code'),
    path('register/', account.register, name='register'),
    path('app1/', include('app1.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
