from django.conf.urls import include, url
from django.contrib import admin
from . import views,api
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^pub/$', views.PublishPubView.as_view(),name="publish_pub"),
    url(r'^list/$', views.PublishListView.as_view(),name="publish_list"),
    url(r'^info/$', views.PublishInfoView.as_view(),name="publish_info"),
    url(r'^delete/$', views.PublishDeleteView.as_view(),name="publish_delete"),
    url(r'^jenkins/api/$', csrf_exempt(api.PublishJenkinsApiView.as_view()),name="publish_jenkins_api"),
    url(r'^get/version/$', api.GetPublishVersionView.as_view(),name="get_publish_version"),
    url(r'^exec/ansible/playbook$', views.PublishAnsiblePlaybookView.as_view(),name="exec_ansible_playbook"),
]
