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
from . import views,user,group,permission,api

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view(),name="user_login"),
    url(r'^logout/$', views.LogoutView.as_view(),name="user_logout"),
    url(r'^users/',include([
        url(r'^modify/',include([
            url(r'^status/$',user.UserModifyStatusView.as_view(),name="users_modify_status"),
            url(r'^group/$',user.UserModifyGroupView.as_view(),name="users_modify_group"),
        ])),
        url(r'^list/$', user.UserListView.as_view(),name="users_list"),
        url(r'^add/$',user.UserAddView.as_view(),name="users_add"),
        url(r'^delete/$',user.UserDeleteView.as_view(),name="users_delete"),
    ])),

    url(r'^user/',include([
        url(r'^extend/add/$',user.UserExtendAddView.as_view(),name="user_extend_add"),
        url(r'^info/',include([
            url(r'^$',user.UserInfoView.as_view(),name="user_info"),
            url(r'^change/$',user.UserInfoChangeView.as_view(),name="user_info_change"),
            url(r'^changepwd/$',user.UserInfoChangePwdView.as_view(),name="user_info_change_passwd"),
        ])),
    ])),

    url(r'^group/',include([
        url(r'^list/$',group.GroupListView.as_view(),name="group_list"),
        url(r'^add/$',group.GroupAddView.as_view(),name="group_add"),
        url(r'^delete/$',group.GroupDeleteView.as_view(),name="group_delete"),
        url(r'^info/$',api.GetGroupInfoView.as_view(),name="get_group_info"),
        url(r'^user/',include([
            url(r'^list/$',group.GroupUserListView.as_view(),name="group_user_list"),
            url(r'^delete/$',group.GroupUserDeleteView.as_view(),name="group_user_delete"),
        ])),
        url(r'^permission/',include([
            url(r'^list/$',group.GroupPermissionListView.as_view(),name="group_permission_list"),
            url(r'^delete/$',group.GroupPermissionDeleteView.as_view(),name="group_permission_delete"),
        ])),
    ])),

    url(r'^permission/',include([
        url(r'^list/$',permission.PermissionListView.as_view(),name="permission_list"),
        url(r'^change/name/$',permission.PermissionChangeNameView.as_view(),name="permission_change_name"),
        url(r'^add/$',permission.PermissionAddView.as_view(),name="permission_add"),
        url(r'^delete/$',permission.PermissionDeleteView.as_view(),name="permission_delete"),
    ])),
]
