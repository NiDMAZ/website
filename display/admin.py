from django.contrib import admin
from .models import FundGoal, MessageBar, Event, BoxWidget

class BoxWidgetsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'content',)
    list_filter = ('order', 'active',)
    list_editable = ('order', 'active', 'content',)
    search_fields = ('order', 'title', 'content')


class EventsAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'event_date', 'photo_url', 'publish_date', 'stop_publish_date')
    list_filter = ('order', 'active', 'event_date',)
    list_editable = ('order', 'active', 'event_date', 'photo_url', 'publish_date', 'stop_publish_date')
    search_fields = ('order', 'title', 'photo_url',)


class GoalFundAdmin(admin.ModelAdmin):
    list_display = ('goal_name', 'goal_amount', 'amount_collected',)
    list_editable = ('goal_amount', 'amount_collected',)


class MessageBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active', 'message', )
    list_editable = ('order', 'active', 'message', )
    list_filter = ('order', 'active')


# Register your models here.
admin.site.register(FundGoal, GoalFundAdmin)
admin.site.register(MessageBar, MessageBarAdmin)
admin.site.register(Event, EventsAdmin)
admin.site.register(BoxWidget, BoxWidgetsAdmin)
