from django.shortcuts import render,reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin,TemplateView):
    template_name = "index.html"

class NoPermissionView(TemplateView):
    template_name = "public/no_permission.html"

    def get_context_data(self,**kwargs):
        context = super(NoPermissionView, self).get_context_data(**kwargs)
        uri_name = self.kwargs.get("next_uri", "index")
        try:
            next_uri = reverse(uri_name)
        except:
            pass
        context['next_uri'] = next_uri
        return context
