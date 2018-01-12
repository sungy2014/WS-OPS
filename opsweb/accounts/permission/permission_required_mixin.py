from django.contrib.auth.mixins import PermissionRequiredMixin as PermissionRequired
from django.shortcuts import redirect


class PermissionRequiredMixin(PermissionRequired):
    
    permission_redirect_url = "index"

    def dispatch(self,request,*args,**kwargs):
        if not self.has_permission():
            return redirect("no_permission",next_uri=self.permission_redirect_url)
        return super(PermissionRequiredMixin,self).dispatch(request,*args,**kwargs)
