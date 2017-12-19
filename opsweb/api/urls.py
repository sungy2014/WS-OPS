
from django.conf.urls import include, url
from django.contrib import admin
from . import views,myapi

urlpatterns = [
    url(r'^get/',include([
        url(r'^idc/',include([
            url(r'^list/$',myapi.get_idc.GetIdcListView.as_view(),name="get_idc_list"),
        ])),
        url(r'^server/',include([
            url(r'^env/',myapi.get_server_env.GetServerEnvView.as_view(),name="get_server_env"),
            url(r'^ips/',myapi.get_server_ips.GetServerIPView.as_view(),name="get_server_ips"),
        ])),
    ])),
    url(r'^post/',include([
        url(r'^idc/',include([
            url(r'^list/$',myapi.get_idc.GetIdcListView.as_view(),name="post_idc_list"),
        ])),
    ])),
]
