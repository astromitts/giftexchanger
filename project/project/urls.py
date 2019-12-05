"""project URL Configuration

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
from django.urls import path
from giftexchanger import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),
    path('exchangedetails/<int:exc_id>/', views.exchange_details, name='exchange_details'),
    path('exchangedetails/<int:exc_id>/edit/', views.exchange_details_edit, name='exchange_details_edit'),
    path('exchange/<int:exc_id>/admin/', views.exchange_admin, name='exchange_admin'),
]
