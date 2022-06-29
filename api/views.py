from django.shortcuts import render
from movies.models import Movie
from reservation.models import PlayingTime, Reservation
from api.utils import get_current_week
from .serializers import MovieSerializer, PlayingTimeSerializer, ReservationSerializer
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
    serializer_class = PlayingTimeSerializer

class ReservationsViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer