from rest_framework import generics, permissions
from rest_framework.viewsets import GenericViewSet
from bookmaker.bets.models import EventCategory
from bookmaker.bets import serializers


class EventCategoryViewSet(generics.ListAPIView, generics.RetrieveAPIView, GenericViewSet):
    queryset = EventCategory.objects.filter(online=True)
    permission_classes = (permissions.AllowAny,)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.EventCategoryListSerializer
        return serializers.EventCategorySerializer
