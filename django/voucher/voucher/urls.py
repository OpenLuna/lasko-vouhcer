"""outfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from manager import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url('', include('social.apps.django_app.urls', namespace='social')),

    url(r'^$', views.login),

    url(r'^getVoucher/(?P<my_code>\w+)', views.getVoucher2),
    url(r'^getVoucher', views.getVoucher2),
    url(r'^useVoucher/(?P<my_code>\w+)/', views.useVoucher),

    url(r'^logout/', views.logout),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
