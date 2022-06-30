from rest_framework import routers
from api.views import MoviesPlayingThisWeekViewSet, MoviesPlayingThisWeekDetailsViewSet, MoviesAPIView

router = routers.DefaultRouter()

router.register(
    "movies-playing-this-week", MoviesPlayingThisWeekViewSet, "assigned_movies_this_week"

)

router.register(
    "movies-playing-time-this-week", MoviesPlayingThisWeekDetailsViewSet, 'movies_playing_time_this_week'
)

router.register(
    "movies", MoviesAPIView, 'movies'
)
