"""base URL Configuration

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
from django.urls import path
from default import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('ping/', views.ping),
    path('category/', views.category),
    path('good_list/', views.good_list),
    path('good_detail/', views.good_detail),
    path('search/', views.search),
    path('good_ana_res/', views.good_ana_res),
    path('good_list/', views.good_list),
    path('list_ana_res/', views.list_ana_res),
    path('top_ana_detail/', views.top_ana_detail)
]
