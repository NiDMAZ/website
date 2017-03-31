from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import datetime

# Create your views here.


def homepage(request):
    return render(request, 'registration/homepage.html', {})


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
