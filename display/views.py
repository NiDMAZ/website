from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import datetime

# Create your views here.


def homepage(request):
    today_date = datetime.datetime.now()

    today_day = today_date.strftime("%d")
    today_month = today_date.strftime("%B")

    return render(request, 'display/homepage.html', {'today_day': today_day,
                                                     'today_month': today_month})


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
