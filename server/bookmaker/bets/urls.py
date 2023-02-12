from django.urls import path
from bookmaker.bets import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'categories', views.EventCategoryViewSet, basename='categories')
