from django.contrib import admin
from .models import FundRaisingEvent, FundGoal

# Register your models here.

admin.site.register(FundRaisingEvent)
admin.site.register(FundGoal)