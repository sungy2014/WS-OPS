
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^pub/',include([
        url(r'^add/$',views.PubWorkFormAddView.as_view(),name="pub_workform_add"),
    ])),

    url(r'^list/$',views.WorkFormListView.as_view(),name="workform_list"),
    url(r'^delete/$',views.WorkFormDeleteView.as_view(),name="workform_delete"),

    url(r'^process/',include([
        url(r'^trace/$',views.ProcessTraceView.as_view(),name="process_trace"),
        url(r'^step/approval$',views.ProcessStepApprovalInfoView.as_view(),name="process_step_approval"),
    ])),

    url(r'^my/',include([
        url(r'^list/$',views.MyWorkFormListView.as_view(),name="my_workform_list"),
        url(r'^approval/$',views.ApprovalWorkFormView.as_view(),name="workform_approval"),
    ])),

    url(r'^info/$',views.WorkFormInfoView.as_view(),name="workform_info"),

    url(r'^upload/',include([
        url(r'^pub/$',views.PubWorkFormUploadView.as_view(),name="pub_workform_upload"),
        url(r'^pub/(?P<filename>[\s\S]*)/$',views.PubWorkFormUploadFilePreviewView.as_view(),name="pub_workform_upload_file_preview"),
    ])),
]
