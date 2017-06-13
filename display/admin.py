from django.contrib import admin
from .models import FundGoal, MessageBar, CarouselEvents, BoxWidget

# Register your models here.
admin.site.register(FundGoal)
admin.site.register(MessageBar)
admin.site.register(CarouselEvents)
admin.site.register(BoxWidget)