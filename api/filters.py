from django_filters.rest_framework import FilterSet
from reservation.models import PlayingTime
from cinemas.models import Seat

class PlayingTimeFilter(FilterSet):
    class Meta:
        model = PlayingTime
        fields = ["assigned_movie__imdb_id", "assigned_movie__name"]


class SeatFilter(FilterSet):
    class Meta:
        model = Seat
        fields = ["halls__id"]