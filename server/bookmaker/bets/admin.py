from django.contrib import admin
from .models import EventCategory, Event, Player, EventPlayer, Bet

admin.site.register(EventCategory)
admin.site.register(Event)
admin.site.register(Player)
admin.site.register(EventPlayer)
admin.site.register(Bet)
