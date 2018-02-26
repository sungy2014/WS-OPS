from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView,ListView,View



class PublishPubView(TemplateView):
    template_name = "publish_pub.html"

    def get_context_data(self):
        context = super(PublishPubView,self).get_context_data()
        print("current_url:",self.request.path)
        print("host_url:",self.request.get_host())
        return context
