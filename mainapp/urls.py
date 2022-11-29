"""mainapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tt/', views.tt, name='tt'),
    path('getdata/', csrf_exempt(views.get_data), name='getdata'),
    path('test/', csrf_exempt(views.test), name='test'),
    path('check_file/', csrf_exempt(views.check_file), name='check_file'),
    path('execute_trade/', csrf_exempt(views.execute_trade), name='execute_trade'),
    path('exit_trade/', csrf_exempt(views.exit_trade), name='exit_trade'),
    path('send_telegram_message/', views.send_telegram_message, name='send_telegram_message'),
    path('token/', views.token_view, name='test'),
    path('user/', views.user_detail, name='user'),
    path('admin/', admin.site.urls),
]
