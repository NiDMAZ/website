from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


# Create your models here.

message_bar_order = ((1, 1), (2, 2), (3, 3), (4, 4))
widget_box_choices = ((1,1), (2,2), (3,3))

class FundRaisingEvent(models.Model):
    fundraising_event = models.CharField(max_length=30)
    goal_date = models.DateField(auto_now=True)
    fund_goal = models.IntegerField()
    fund_collection = models.IntegerField()

    def __str__(self):
        return self.fundraising_event


class FundGoal(models.Model):
    goal_name = models.CharField(max_length=20)
    goal_amount = models.IntegerField()
    amount_collected = models.IntegerField()

    def __str__(self):
        return self.goal_name

class MessageBar(models.Model):
    title = models.CharField(max_length=16)
    message = models.CharField(max_length=32)
    active = models.BooleanField()
    order = models.IntegerField(choices=message_bar_order)

    def __str__(self):
        return '{}-{}: {}'.format(self.order, self.title, self.active)


class CarouselEvents(models.Model):
    title = models.CharField(max_length=32)
    event_date = models.DateField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    active = models.BooleanField()
    photo_url = models.CharField(max_length=512)
    order = models.IntegerField()

    def __str__(self):
        active = "ACTIVE" if self.active else "INACTIVE"
        return '[Order:{}] [Title: {}] [EventDate: {}] [Status: {}]'.format(self.order, self.title, self.event_date, active)


class BoxWidget(models.Model):
    title = models.CharField(max_length=32)
    active = models.BooleanField()
    order = models.IntegerField(choices=widget_box_choices)
    content = models.TextField(max_length=4096)

    def __str__(self):
        active = "ACTIVE" if self.active else "INACTIVE"
        return '[Order:{}] [Title: {}] [Status: {}]'.format(self.order, self.title, active)