from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
# Create your views here.
from api.serializers import PlayingTimeSerializer, MovieSerializer
from api.utils import get_current_week
from reservation.models import PlayingTime
from movies.models import Movie


class MoviesPlayingThisWeekViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ModelViewSet):
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeSerializer
