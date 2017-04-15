from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import datetime
from .forms import VolunteerForm
from .amo_modules import FundRaisingStatus

# Create your views here.


def homepage(request):
    fund_details = FundRaisingStatus(goal_name='annual')

    page_context = {
        'today_day': datetime.datetime.now().strftime("%d"),
        'today_month': datetime.datetime.now().strftime("%B"),
        'goal_amount':  fund_details.goal_amount,
        'goal_percent': fund_details.percent,
        'goal_collected': fund_details.amount_collected,
        'goal_remain': fund_details.amount_remain}

    return render(request, 'display/homepage.html', page_context)


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