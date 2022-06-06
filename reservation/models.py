from django.contrib.auth.models import User
from django.db import models
from movies.models import Movie
from cinemas.models import *
from datetime import datetime, timedelta
# Create your models here.


class PlayingTime(models.Model):
    assigned_movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    assigned_hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Movie {self.assigned_movie} in {self.assigned_hall}'

    def add_time(self):
        time = datetime(
            year=self.start_time.year,
            month=self.start_time.month,
            day=self.start_time.day,
            hour=self.start_time.hour,
            minute=self.start_time.minute,
            second=self.start_time.second,
        )
        return time + timedelta(minutes=self.assigned_movie.length_min)

    def save(self, *args, **kwargs):
        self.end_time = self.add_time()
        super().save(*args, **kwargs)


class Reservation(models.Model):
    user = models.ForeignKey(User,  null=True, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, null=True, on_delete=models.CASCADE)
    playing_time = models.ForeignKey(PlayingTime, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}/ {self.seat}/ {self.playing_time.assigned_movie}'
