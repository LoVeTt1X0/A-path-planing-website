"""ruanjian URL Configuration

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
from django.contrib import admin
from django.urls import path,re_path
from django.conf import settings
from django.views.static import serve
import os
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('mainwin/',views.mainwin),
    path('mainwin2/', views.mainwin2),
    path('mainwin3/', views.mainwin3),
    path('mainwin4/', views.mainwin4),
    path('mainwin5/', views.mainwin5),
    path('path_choose/', views.path_choose),
    path('path_choose_err/',views.path_choose_err),
    path('path_choose_res/',views.path_choose_res),
    path('path_choose_res2/', views.path_choose_res2),
    path('path_choose_busy/', views.path_choose_busy),
    re_path(r'^image/(?P<path>.*)$', serve, {'document_root': 'D:/ruanjian/image'}),
]
