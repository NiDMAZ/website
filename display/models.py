from __future__ import unicode_literals

from django.db import models

# Create your models here.

class FundRaisingEvent(models.Model):
    fundraising_event = models.CharField(max_length=30)
    goal_date = models.DateField(auto_now=True)
    fund_goal = models.IntegerField()
    fund_collection = models.IntegerField()

    def __str__(self):
        return self.fundraising_event
