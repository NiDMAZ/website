from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
import datetime
from .forms import VolunteerForm
from .amo_modules import FundRaisingStatus, MessageBarMessages, as_currency,\
    is_not_june, CarouselPosts, BoxWidgets

# Create your views here.


def homepage(request):
    fund_details = FundRaisingStatus(goal_name='annual')
    msg_bar = MessageBarMessages()
    events = CarouselPosts()
    widgets = BoxWidgets()

    page_context = {
        'today_day': datetime.datetime.now().strftime("%d"),
        'today_month': datetime.datetime.now().strftime("%B"),
        'goal_amount':  as_currency(fund_details.goal_amount),
        'goal_amount_num': fund_details.goal_amount,
        'goal_percent': fund_details.percent,
        'goal_collected': as_currency(fund_details.amount_collected),
        'goal_collected_num': fund_details.amount_collected,
        'goal_remain': as_currency(fund_details.amount_remain),
        'messages': msg_bar.messages,
        'events': events.get_events(),
        'is_not_june': is_not_june(),
        'widgets': widgets.get_posts()}

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