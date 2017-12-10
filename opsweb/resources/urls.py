
from django.conf.urls import include, url
from django.contrib import admin
from . import views,server,idc

urlpatterns = [
    url(r'^server/',include([
        url(r'^aliyun/',include([
            url(r'^list/$',server.ServerAliyunListView.as_view(),name="server_aliyun_list"),
            url(r'^add/$',server.ServerAliyunAddView.as_view(),name="server_aliyun_add"),
            url(r'^refresh/$',server.ServerAliyunRefreshView.as_view(),name="server_aliyun_refresh"),
            url(r'^info/$',server.ServerAliyunInfoView.as_view(),name="server_aliyun_info"),
        ])),
    ])),
    url(r'^idc/',include([
        url(r'^list/$',idc.IdcListView.as_view(),name="idc_list"),
        url(r'^add/$',idc.IdcAddView.as_view(),name="idc_add"),
        url(r'^delete/$',idc.IdcDeleteView.as_view(),name="idc_delete"),
    ])),
]
