from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(
    "movies_playing_this_week", MoviesPlayingThisWeekViewSet, "assigned_movies_this_week"
)

router.register(
    "assigned_movies_playing_time_this_week", MoviesPlayingThisWeekDetailsViewSet, 'assigned_movies_playing_time_this_week'
)