from django.shortcuts import render
from movies.models import Movie
from reservation.models import PlayingTime
from api.utils import get_current_week
from .serializers import MovieSerializer
from rest_framework import viewsets
# Create your views here.


class MoviesPlayingThisWeekViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer