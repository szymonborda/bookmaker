from django.utils import timezone
from rest_framework import serializers
from bookmaker.bets.models import Bet, EventCategory, Event, EventPlayer, Player


class EventCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = [
            "id",
            "name",
            "description",
        ]


class EventCategorySerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = EventCategory
        fields = [
            "id",
            "name",
            "description",
            "events",
        ]

    def get_events(self, obj):
        return EventSerializer(obj.get_online_events(), many=True).data


class EventSerializer(serializers.ModelSerializer):
    event_players = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "category",
            "start_time",
            "end_time",
            "event_players",
        ]

    def get_event_players(self, obj):
        return EventPlayerSerializer(obj.get_event_players(), many=True).data


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = [
            "id",
            "name",
            "description",
        ]


class EventPlayerSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()

    class Meta:
        model = EventPlayer
        fields = [
            "id",
            "player",
            "odds",
            "event",
        ]


class BetSerializer(serializers.ModelSerializer):
    event = serializers.SerializerMethodField(read_only=True)
    possible_win = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bet
        fields = [
            "id",
            "wager",
            "event_player",
            "possible_win",
            "event",
        ]

    def validate(self, attrs):
        wager = attrs.get('wager')
        event_player = attrs.get('event_player')
        if wager <= 0:
            raise serializers.ValidationError({'wager': 'Invalid wager'})
        if wager > self.context['request'].user.balance:
            raise serializers.ValidationError({'wager': 'Insufficient funds'})
        if event_player.event.online is False:
            raise serializers.ValidationError('Event is not online')
        if event_player.event.start_time < timezone.now():
            raise serializers.ValidationError('Event has already started')
        return super().validate(attrs)

    def create(self, validated_data):
        wager = validated_data.get('wager')
        event_player = validated_data.get('event_player')
        account = self.context['request'].user
        account.balance -= wager
        account.save()
        return Bet.objects.create(
            account=account,
            event_player=event_player,
            wager=wager,
        )

    def get_event(self, obj):
        return EventSerializer(obj.get_event()).data

    def get_possible_win(self, obj):
        return obj.get_possible_win()
