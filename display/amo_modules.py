import logging
import pytz
from .models import FundGoal, MessageBar, Event, BoxWidget
import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


def percentage(part, whole):
  return 100 * float(part)/float(whole)


def as_currency(amount):
    if amount >= 0:
        return '${:,}'.format(amount)
    else:
        return '-${:,.2f}'.format(-amount)


class FundRaisingStatus(object):
    def __init__(self, goal_name):
        self._goal_name = goal_name
        self.goal_details = self.get_fundraising_goal(goal_name=self._goal_name)

    def get_fundraising_goal(self, goal_name):
        goal_status = FundGoal.objects.filter(goal_name=goal_name)
        len_goal = len(goal_status)

        DEFAULT = {'amount_collected': 50,
                   'goal_amount': 100,
                   'goal_name': '{}-DEFAULT'.format(goal_name)}

        if len_goal > 0 and len_goal < 2:
            logger.info('Found Fund raising goal: {!r}'.format(goal_name))

        elif len_goal == 0:
            logger.error('Did not find any goals matching {!r}'.format(goal_name))
            return DEFAULT

        elif len_goal > 1:
            logger.warning('Found multiple matches for goal name {!r}'.format(goal_name))

        return goal_status.values()[0]

    @property
    def percent(self):
        return percentage(part=self.goal_details.get('amount_collected'), whole=self.goal_details.get('goal_amount'))

    @property
    def goal_name(self):
        return self.goal_details.get('goal_name')

    @property
    def goal_amount(self):
        return self.goal_details.get('goal_amount')

    @property
    def amount_collected(self):
        return self.goal_details.get('amount_collected')

    @property
    def amount_remain(self):
        return self.goal_details.get('goal_amount') - self.goal_details.get('amount_collected')


class MessageBarMessages(object):
    def __init__(self):
        """ I am filtering messages that are tagged active, then i order by the most recent message by the message id 
        then by the message order.
        This  then allow me to get onl the recent message for each order
        """
        self._messages = None

    @property
    def messages(self):
        message_string = ''
        messages = self.get_latest_messages()
        len_messages = len(messages)
        msg_sep = '<b class="msg-sep">|</b>' if len_messages > 1 else ''
        if len_messages > 0:
            msg_count = 0
            for msg in messages:
                msg_count += 1
                if msg_count != len_messages:
                    message_string += '{msg} {sep} '.format(msg=msg.message, sep=msg_sep)
                else:
                    message_string += '{msg} {sep} '.format(msg=msg.message, sep='')
        else:
            message_string = datetime.date.today()

        logger.info(message_string)
        return message_string

    def get_active_messages(self):
        active_msg = MessageBar.objects.filter(active=True).order_by('order', '-id')
        logger.info('Active messages {}'.format(active_msg))
        return active_msg

    def get_latest_messages(self):
        message_list = []
        logger.info('Getting Active Messages')
        active_messages = self.get_active_messages()
        if len(active_messages) > 0:
            for msg_order in range(1,5):
               logger.info('Checking for Order# {!r}'.format(msg_order))
               msg = active_messages.filter(order=msg_order).order_by('-id')
               if len(msg)  > 0:
                   logger.info('Found 1 or more message for Order# {!r}'.format(msg_order))
                   message_list.append(msg[0])

        logger.info('Returning list of messages: {}'.format(message_list))
        return message_list


class EventPosts(object):
    def __init__(self):
        # TODO:
        # Pass non-naive timezone
        # GRABBING THE TIME ZONE IN THE settings.py file
        self.date_time_now = datetime.datetime.now(tz=pytz.UTC).strftime('%Y-%m-%d %H:%M:%S')
        self.active_events = (Event.objects.filter(stop_publish_date__gt=self.date_time_now,
                                                  active=True,
                                                  publish_date__lte=self.date_time_now) | Event.objects.filter(stop_publish_date=None,
                                                  active=True,
                                                  publish_date__lte=self.date_time_now)).order_by('order',
                                                                                            'event_date')

    def get_events(self):
        logger.info('[EventsPosts] Returning events that has published greater than {} and stop publish date less than {}'.format(self.date_time_now, self.date_time_now))
        # TODO:(Safraz) Have this check if the event order has a duplicate and take most recent
        return self.active_events


def is_not_june():
    return datetime.date.today() < datetime.date(2017,6,1)


class BoxWidgets(object):
    def __init__(self):
        self.active_widgets = BoxWidget.objects.filter(active=True).order_by('order')

    def get_posts(self):
        if len(self.active_widgets) > 0:
            return self.active_widgets
        else:
            return None

def format_khateeb(khateeb):
    if khateeb is None:
        return None
    elif khateeb.values()[0] is None:
        return None
    else:
        return {'name': khateeb.values()[0], 'date': khateeb.keys()[0].strftime("%B %d, %Y")}
