from rest_framework import routers
from api.views import MoviesPlayingThisWeekViewSet, MoviesPlayingThisWeekDetailsViewSet,\
    MoviesAPIView, PlayingTimeViewSet, ReservationsViewSet, HallViewSet

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

router.register(
    "playing-time", PlayingTimeViewSet, 'playing_time'
)

router.register(
    "reservations", ReservationsViewSet, 'reservations'
)
router.register(
    "halls", HallViewSet, 'halls'
)
