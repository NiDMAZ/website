from django.contrib import admin
from .models import FundGoal, MessageBar, CarouselEvents, BoxWidget

class BoxWidgetsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'content',)
    list_filter = ('order', 'active',)
    list_editable = ('order', 'active', 'content',)
    search_fields = ('order', 'title', 'content')



class CarouselEventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'event_date', 'created_date', 'photo_url')
    list_filter = ('order', 'active', 'event_date',)
    list_editable = ('order', 'active', 'event_date', 'photo_url',)
    search_fields = ('order', 'title', 'photo_url',)


class GoalFundAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'goal_amount', 'amount_collected',)
    list_editable = ('goal_name', 'goal_amount', 'amount_collected',)


class MessageBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'message', )
    list_editable = ('title', 'order', 'active', 'message', )
    list_filter = ('order', 'active')


# Register your models here.
admin.site.register(FundGoal, GoalFundAdmin)
admin.site.register(MessageBar, MessageBarAdmin)
admin.site.register(CarouselEvents, CarouselEventsAdmin)
admin.site.register(BoxWidget, BoxWidgetsAdmin)
