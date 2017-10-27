"""opsweb URL Configuration

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
from . import views,server,idc

urlpatterns = [
    url(r'^server/',include([
        url(r'^list/$',server.ServerListView.as_view(),name="server_list"),
    ])),
    url(r'^idc/',include([
        url(r'^list/$',idc.IdcListView.as_view(),name="idc_list"),
        url(r'^add/$',idc.IdcAddView.as_view(),name="idc_add"),
        url(r'^delete/$',idc.IdcDeleteView.as_view(),name="idc_delete"),
    ])),
]
