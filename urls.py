"""Proyecto_Sars_CoV URL Configuration

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
#----Librerias---
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
#importamos las funciones del scrit views
from quickstart.views import inicio, form, result, about, contact, error, explore 
from quickstart.views import agps, geo, nrf, str_an, tem_an, descriptives

#------configuracion de las URL----
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('form/', form),
    path('about_us/', about),
    path('contact/', contact),
    path('form/error', error),
    path('results/', result),
    path('explore_haplotypes/', explore),
    path('results/agps', agps),
    path('results/Geo_An', geo),
    path('results/NRFp', nrf),
    path('results/str_an', str_an),
    path('results/Tem_an', tem_an),
    path('results/descriptives', descriptives),
    #agregamos para la direccion de archivos estaticos y media
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)