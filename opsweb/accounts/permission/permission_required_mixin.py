from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect


class PermissionRequiredMixin(PermissionRequired):
    
    permission_redirect_url = "dashboard"

    def dispatch(self,request,*args,**kwargs):
        if not self.has_permission():
            return redirect(self.permission_redirect_url)
        return super(PermissionRequiredMixin,self).dispatch(request,*args,**kwargs)
