from .models import FundGoal, MessageBar
import datetime


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
            print 'Found Fund raising goal: {!r}'.format(goal_name)

        elif len_goal == 0:
            print 'Did not find any goals matching {!r}'.format(goal_name)
            return DEFAULT

        elif len_goal > 1:
            print 'Found multiple matches for goal name {!r}'.format(goal_name)

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

        print message_string
        return message_string

    def get_active_messages(self):
        active_msg = MessageBar.objects.filter(active=True).order_by('order', '-id')
        print 'Active messages {}'.format(active_msg)
        return active_msg

    def get_latest_messages(self):
        message_list = []
        print 'Getting Active Messages'
        active_messages = self.get_active_messages()
        if len(active_messages) > 0:
            for msg_order in range(1,5):
               print 'Checking for Order# {!r}'.format(msg_order)
               msg = active_messages.filter(order=msg_order).order_by('-id')
               if len(msg)  > 0:
                   print 'Found 1 or more message for Order# {!r}'.format(msg_order)
                   message_list.append(msg[0])

        print 'Returning list of messages: {}'.format(message_list)
        return message_list


