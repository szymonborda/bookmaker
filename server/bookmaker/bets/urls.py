from bookmaker.bets import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.EventCategoryViewSet, basename='categories')
router.register(r'bets', views.BetViewSet, basename='bets')
router.register(r'events', views.EventViewSet, basename='events')
