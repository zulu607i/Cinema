from rest_framework.exceptions import ValidationError

from cinemas.models import MovieTheater, Hall, Seat
from reservation.models import PlayingTime, Reservation
from locations.models import *
from movies.models import Movie
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username']

class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ['name']


class CitySerializer(serializers.ModelSerializer):


    class Meta:
        model = City
        fields = ['name']


class StreetSerializer(serializers.ModelSerializer):
    county = CountySerializer
    city = CitySerializer

    class Meta:
        model = Street
        fields = ['name']


class MovieTheaterSerializer(serializers.ModelSerializer):
    county = CountySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    street = StreetSerializer(read_only=True)

    class Meta:
        model = MovieTheater
        fields = ['name', 'county', 'city', 'street']


class HallSerializer(serializers.ModelSerializer):
    cinema = MovieTheaterSerializer(source='movie_theater', read_only=True)

    class Meta:
        model = Hall
        fields = ['id', 'name', 'movie_theater', 'cinema']


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'is_occupied', 'seat_name', 'halls']


class MovieSerializer(serializers.ModelSerializer):
    poster_path = serializers.CharField(source='poster')

    class Meta:
        model = Movie
        exclude = ['user', 'is_scheduled', 'poster']


class PlayingTimeWithDetailsSerializer(serializers.ModelSerializer):
    hall = HallSerializer(source='assigned_hall')
    movie = MovieSerializer(source="assigned_movie")

    class Meta:
        model = PlayingTime
        fields = ['movie', 'hall', 'get_date', 'get_time']


class PlayingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayingTime
        fields = ['id', 'start_time', 'end_time', 'assigned_movie', 'assigned_hall']


class ReservationSerializer(serializers.ModelSerializer):
    playing_time_name = serializers.CharField(source='playing_time', read_only=True)
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user',  'playing_time', 'playing_time_name', 'seat', 'is_confirmed', 'movie']


class UserReservationSerializer(serializers.ModelSerializer):
    movie = serializers.CharField(source='playing_time.assigned_movie.name', read_only=True)
    playing_time_name = serializers.CharField(source='playing_time', read_only=True)
    reservation_is_confirmed = serializers.BooleanField(source='is_confirmed', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'playing_time', 'playing_time_name', 'seat', 'reservation_is_confirmed', 'movie']


class ChangeReservationSeatStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_name', 'is_occupied', 'halls']








