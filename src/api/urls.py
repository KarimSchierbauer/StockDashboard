"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework.authtoken.views import obtain_auth_token

from core.views import TestView, SymbolView, StockView, SymbolViewByName, StocksViewByName

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('admin/', admin.site.urls),
    path('', TestView.as_view(), name='test'),
    path('symbol/', SymbolView.as_view(), name='symbol'),
    path('symbolsearch/<str:pk>/', SymbolViewByName.as_view(), name='symbolname'),
    path('stocksearch/<str:pk>/', StocksViewByName.as_view(), name='stockname'),
    path('stock/', StockView.as_view(), name='stock'),
    path('api/token/', obtain_auth_token, name='obtain-token')
]
