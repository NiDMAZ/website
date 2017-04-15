from .models import FundGoal

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



def percentage(part, whole):
  return 100 * float(part)/float(whole)