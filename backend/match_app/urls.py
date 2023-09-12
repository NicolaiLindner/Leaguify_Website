from django.urls import path
from .views import fetch_game_durations

urlpatterns = [
    path('api/game_durations/', fetch_game_durations, name='fetch_game_durations'),
]
