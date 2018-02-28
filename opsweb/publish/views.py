from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView,View
from dashboard.utils.wslog import wslog_error,wslog_info



class PublishPubView(TemplateView):
    template_name = "publish_pub.html"

    def get_context_data(self):
        context = super(PublishPubView,self).get_context_data()
        wslog_info().info("请求的url: %s" %(self.request.get_host()))
        wslog_info().info("请求的端口: %s" %(self.request.get_port()))
        wslog_info().info("转发: %s" %(self.request.META))
        return context
