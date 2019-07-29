"""zed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from zed import settings
from accounts import views
from product.views import redirect_to_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/', include('category.urls', namespace='category')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('common/', include('common.urls', namespace='common')),
    path('currency/', include('currency.urls', namespace='currency')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('login/', views.user_login, name='user_login'),
    path('product/', include('product.urls', namespace='product')),
    path('', redirect_to_login, name='test')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)