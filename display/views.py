from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import datetime
from .forms import VolunteerForm
from .models import FundGoal

# Create your views here.


def homepage(request):
    today_date = datetime.datetime.now()
    today_day = today_date.strftime("%d")
    today_month = today_date.strftime("%B")
    fund_percent = 60
    fund_details = FundGoal.objects.filter(goal_name='annual').values()[0]
    goal_amount = ''
    amount_collected = ''
    amount_remain = ''


    return render(request, 'display/homepage.html', {'today_day': today_day,
                                                     'today_month': today_month,
                                                     'fund_percent': fund_percent,
                                                     'fund_details': fund_details})


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def volunteer_page(request):
    context = {
        'form' : VolunteerForm(),
        'page_title': 'Volunteer Form',
        'button_text': 'Submit',
        'page_body': 'Some Program Voluneteer form'
    }

    return render(request, 'display/request_page.html', context)


def blood_drive(request):
    context = {
        'form' : VolunteerForm(),
        'page_title': 'Blood Drive',
        'button_text': 'Donate',
        'page_body': 'blood drive donation'
    }

    return render(request, 'display/request_page.html', context)