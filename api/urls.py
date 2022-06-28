from rest_framework import routers

from api.views import MoviesPlayingThisWeekViewSet

router = routers.DefaultRouter()

router.register(
    "movies-playing-this-week", MoviesPlayingThisWeekViewSet, "assigned_movies_this_week"
)
