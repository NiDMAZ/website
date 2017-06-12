from django.contrib import admin
from .models import FundGoal, MessageBar, CarouselEvents, BoxWidgets

# Register your models here.
admin.site.register(FundGoal)
admin.site.register(MessageBar)
admin.site.register(CarouselEvents)
admin.site.register(BoxWidgets)