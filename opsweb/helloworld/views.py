from django.shortcuts import render

from django.http import HttpResponse
from datetime import * 


# Create your views here.

def hello_world(request,month,year):
#	print(time_str)
#	time_now = datetime.now()
#	time_change = timedelta(hours=int(time_str))
#	time = time_now + time_change
	return HttpResponse("%s%s" %(year,month))
