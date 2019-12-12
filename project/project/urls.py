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
from giftexchanger.views import app, session

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.user_dashboard, name='user_dashboard'),
    path('login/', session.login_handler, name='login_handler'),
    path('exchangedetails/<int:exc_id>/', app.exchange_details, name='exchange_details'),
    path('exchangedetails/<int:exc_id>/edit/', app.exchange_details_edit, name='exchange_details_edit'),
    path('exchange/<int:exc_id>/admin/', app.exchange_admin, name='exchange_admin'),
    path('exchange/<int:exc_id>/admin/edit/', app.exchange_admin_edit, name='exchange_admin_edit'),
]
