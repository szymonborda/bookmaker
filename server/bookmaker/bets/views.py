from rest_framework import generics, permissions
from rest_framework.viewsets import GenericViewSet
from bookmaker.bets.models import EventCategory, Bet, Event
from bookmaker.bets import serializers


class EventCategoryViewSet(generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    queryset = EventCategory.objects.filter(online=True)
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EventCategoryListSerializer
        return serializers.EventCategorySerializer


class BetViewSet(generics.CreateAPIView, generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    serializer_class = serializers.BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(account=self.request.user)

    def get_object(self):
        return generics.get_object_or_404(Bet, account=self.request.user, pk=self.kwargs['pk'])


class EventViewSet(generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    queryset = Event.objects.filter(online=True)
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return generics.get_object_or_404(Event, online=True, pk=self.kwargs['pk'])
