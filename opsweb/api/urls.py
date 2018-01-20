
from django.conf.urls import include, url
from django.contrib import admin
from . import views,myapi

urlpatterns = [
    url(r'^get/',include([
        url(r'^idc/',include([
            url(r'^list/$',myapi.get_idc.GetIdcListView.as_view(),name="get_idc_list"),
        ])),
        url(r'^server/',include([
            url(r'^env/',myapi.get_server_related.GetServerEnvView.as_view(),name="get_server_env"),
            url(r'^ips/',myapi.get_server_related.GetServerIPView.as_view(),name="get_server_ips"),
            url(r'^statistic/',myapi.get_dashboard_info.GetServerStatisticView.as_view(),name="get_server_statistic"),
        ])),
        url(r'^cmdb/',include([
            url(r'^env/',myapi.get_cmdb_related.GetCmdbEnvView.as_view(),name="get_cmdb_env"),
            url(r'^type/',myapi.get_cmdb_related.GetCmdbTypeView.as_view(),name="get_cmdb_type"),
            url(r'^way/',myapi.get_cmdb_related.GetCmdbWayView.as_view(),name="get_cmdb_way"),
            url(r'^name/',myapi.get_cmdb_related.GetCmdbNameView.as_view(),name="get_cmdb_name"),
            url(r'^statistic/',myapi.get_dashboard_info.GetCmdbStatisticView.as_view(),name="get_cmdb_statistic"),
        ])),
    ])),
    url(r'^post/',include([
        url(r'^idc/',include([
            url(r'^list/$',myapi.get_idc.GetIdcListView.as_view(),name="post_idc_list"),
        ])),
    ])),
]
