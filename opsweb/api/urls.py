
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
        url(r'^cmdb/',include([
            url(r'^env/',myapi.get_cmdb_related.GetCmdbEnvView.as_view(),name="get_cmdb_env"),
            url(r'^type/',myapi.get_cmdb_related.GetCmdbTypeView.as_view(),name="get_cmdb_type"),
            url(r'^way/',myapi.get_cmdb_related.GetCmdbWayView.as_view(),name="get_cmdb_way"),
        ])),
    ])),
    url(r'^post/',include([
        url(r'^idc/',include([
            url(r'^list/$',myapi.get_idc.GetIdcListView.as_view(),name="post_idc_list"),
        ])),
    ])),
]
