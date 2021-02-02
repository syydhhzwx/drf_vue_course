"""edu_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
import xadmin
# from import_export.admin import DEFAULT_FORMATS
# from import_export.admin import SKIP_ADMIN_LOG

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from xadmin.plugins import xversion    # 导入 xadmin需要

xversion.register_models()             # 导入 xadmin需要

urlpatterns = [
    # 静态文件图片 url
    url(r'media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # path('admin/', admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path('admin/', xadmin.site.urls),
    path('home/', include('home.urls')),
    path('user/', include('user.urls')),
    path('course/', include('course.urls')),
    path('cart/', include('cart.urls')),
    path('pay/', include('payments.urls')),
]
