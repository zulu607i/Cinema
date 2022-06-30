from django_filters.rest_framework import FilterSet
from reservation.models import PlayingTime

class PlayingTimeFilter(FilterSet):
    class Meta:
        model = PlayingTime
        fields = ["assigned_movie__imdb_id", "assigned_movie__name"]