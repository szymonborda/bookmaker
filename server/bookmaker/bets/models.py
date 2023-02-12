from django.db import models


class EventCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    online = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Event Categories'

    def __str__(self):
        return self.name

    def get_events(self):
        return Event.objects.filter(category=self)

    def get_online_events(self):
        return Event.objects.filter(category=self, online=True)


class Player(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_event_players(self):
        return EventPlayer.objects.filter(event=self)


class EventPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.player.name} - {self.event.name} - {self.odds}'


class Bet(models.Model):
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    event_player = models.ForeignKey(EventPlayer, on_delete=models.CASCADE)
    wager = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.event_player.player.name} - {self.event_player.event.name} - {self.event_player.odds} - {self.wager}'

    def get_event(self):
        return self.event_player.event

    def get_possible_win(self):
        return self.wager * self.event_player.odds
