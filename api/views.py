from django.shortcuts import render
from movies.models import Movie
from reservation.models import PlayingTime
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeWithDetailsSerializer, PlayingTimeSerializer
from rest_framework import viewsets
# Create your views here.


class MoviesPlayingThisWeekViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ModelViewSet):
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeWithDetailsSerializer


class PlayingTimeViewSet(viewsets.ModelViewSet):
    queryset = PlayingTime.objects.order_by('start_time')
    serializer_class = PlayingTimeSerializer
