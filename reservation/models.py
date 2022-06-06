from django.contrib.auth.models import User
from django.db import models
from movies.models import Movie
from cinemas.models import *
# Create your models here.


class Reservation(models.Model):
    user = models.ForeignKey(User,  null=True, on_delete=models.SET_NULL)
    movie = models.ForeignKey(Movie, null=True, on_delete=models.SET_NULL)
    movie_theater = models.ForeignKey(MovieTheater, null=True, on_delete=models.SET_NULL)
    seat = models.OneToOneField(Seat, null=True, on_delete=models.SET_NULL)
    date = models.DateField(auto_now_add=False, auto_now=False, null=True)
    hour = models.TimeField(auto_now_add=False, auto_now=False, null=True)

    def __str__(self):
        return f'{self.movie}'
