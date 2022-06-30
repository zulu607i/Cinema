from cinemas.models import MovieTheater, Hall, Seat
from reservation.models import PlayingTime, Reservation
from locations.models import *
from movies.models import Movie
from rest_framework import serializers


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
    county = CountySerializer()
    city = CitySerializer()
    street = StreetSerializer()

    class Meta:
        model = MovieTheater
        fields = ['name', 'county', 'city', 'street']


class HallSerializer(serializers.ModelSerializer):
    cinema = MovieTheaterSerializer(source='movie_theater')
    class Meta:
        model = Hall
        fields = ['name', 'cinema',]


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ['__all__']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['user', 'is_scheduled']


class PlayingTimeWithDetailsSerializer(serializers.ModelSerializer):
    hall = HallSerializer(source='assigned_hall')
    movie = MovieSerializer(source="assigned_movie")

    class Meta:
        model = PlayingTime
        fields = ['movie', 'hall', 'get_date', 'get_time']

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'



class PlayingTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlayingTime
        fields = '__all__'
