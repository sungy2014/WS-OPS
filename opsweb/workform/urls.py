
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^pub/',include([
        url(r'^add/$',views.PubWorkFormAddView.as_view(),name="pub_workform_add"),
    ])),
    url(r'^list/$',views.WorkFormListView.as_view(),name="workform_list"),
    url(r'^my/$',views.MyWorkFormListView.as_view(),name="my_workform"),

    url(r'^upload/',include([
        url(r'^pub/$',views.PubWorkFormUploadView.as_view(),name="pub_workform_upload"),
        url(r'^pub/(?P<filename>[\s\S]*)/$',views.PubWorkFormUploadFilePreviewView.as_view(),name="pub_workform_upload_file_preview"),
    ])),
]
