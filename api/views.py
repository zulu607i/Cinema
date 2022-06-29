from django.shortcuts import render
from movies.models import Movie
from reservation.models import PlayingTime
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeSerializer
from rest_framework import viewsets, generics
# Create your views here.


class MoviesPlayingThisWeekViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.filter(
        pk__in=PlayingTime.objects.filter(
            start_time__range=get_current_week()
        ).values_list("assigned_movie", flat=True)
    )
    serializer_class = MovieSerializer


class MoviesPlayingThisWeekDetailsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlayingTime.objects.filter(start_time__range=get_current_week())
    serializer_class = PlayingTimeSerializer


class MoviesAPIView(viewsets.ModelViewSet):
    queryset = Movie.objects.order_by('id')
    serializer_class = MovieSerializer


