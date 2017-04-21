from django.contrib import admin
from .models import FundGoal, MessageBar, Events

# Register your models here.
admin.site.register(FundGoal)
admin.site.register(MessageBar)
admin.site.register(Events)