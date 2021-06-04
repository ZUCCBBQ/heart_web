"""heart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url
from detetction import views as detection_views
from django.urls import path,re_path
from django.views.static import serve
import os


urlpatterns = [
    path("",detection_views.index),
    url(r'^index',detection_views.index,name='index'),
    url(r'^single',detection_views.single,name='single'),
    url(r'^login',detection_views.login,name='login'),
    url(r'^register',detection_views.register,name='register'),
    url(r'^upload',detection_views.upload,name='upload'),
    url(r'^process',detection_views.login_process,name='process'),
    url(r'^logout',detection_views.logout,name='logout'),
    url(r'^result',detection_views.result,name='result'),
    url(r"^video_upload",detection_views.video_upload,name="video_upload"),
    url(r'^heartregister',detection_views.heartregister,name='heartregister'),
    url('admin/', admin.site.urls),
    url(r'^image/(?P<path>.*)$', serve, {'document_root': "F:\\heart_upload\\"}),

]
