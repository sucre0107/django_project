from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [


    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 用于配置静态文件的访问路径

