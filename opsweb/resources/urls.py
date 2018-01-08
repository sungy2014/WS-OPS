
from django.conf.urls import include, url
from django.contrib import admin
from . import views,server,idc,cmdb

urlpatterns = [
    url(r'^server/',include([
        url(r'^aliyun/',include([
            url(r'^list/$',server.ServerAliyunListView.as_view(),name="server_aliyun_list"),
            url(r'^add/$',server.ServerAliyunAddView.as_view(),name="server_aliyun_add"),
            url(r'^refresh/$',server.ServerAliyunRefreshView.as_view(),name="server_aliyun_refresh"),
            url(r'^info/$',server.ServerAliyunInfoView.as_view(),name="server_aliyun_info"),
            url(r'^update/$',server.ServerAliyunUpdateView.as_view(),name="server_aliyun_update"),
        ])),
        url(r'^delete/$',server.ServerDeleteView.as_view(),name="server_delete"),
        url(r'^idc/',include([
            url(r'^list/$',server.ServerIdcListView.as_view(),name="server_idc_list"),
            url(r'^add/$',server.ServerIdcAddView.as_view(),name="server_idc_add"),
            url(r'^update/$',server.ServerIdcUpdateView.as_view(),name="server_idc_update"),
        ])),
    ])),
    url(r'^idc/',include([
        url(r'^list/$',idc.IdcListView.as_view(),name="idc_list"),
        url(r'^add/$',idc.IdcAddView.as_view(),name="idc_add"),
        url(r'^change/$',idc.IdcChangeView.as_view(),name="idc_change"),
        url(r'^delete/$',idc.IdcDeleteView.as_view(),name="idc_delete"),
    ])),
    url(r'^cmdb/',include([
        url(r'^list/$',cmdb.CmdbListView.as_view(),name="cmdb_list"),
        url(r'^add/$',cmdb.CmdbAddView.as_view(),name="cmdb_add"),
        url(r'^change/$',cmdb.CmdbChangeView.as_view(),name="cmdb_change"),
        url(r'^info/$',cmdb.CmdbInfoView.as_view(),name="cmdb_info"),
        url(r'^delete/$',cmdb.CmdbDeleteView.as_view(),name="cmdb_delete"),
    ])),
]
