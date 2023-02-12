from rest_framework import serializers
from bookmaker.bets.models import EventCategory, Event, EventPlayer, Player


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
    players = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "description",
            "category",
            "start_time",
            "end_time",
            "players",
        ]

    def get_players(self, obj):
        return EventPlayerSerializer(obj.get_players(), many=True).data


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
