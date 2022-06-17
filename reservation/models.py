from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

    class Meta:
        unique_together = ['assigned_hall', 'start_time']

    def __str__(self):
        return f'Cinema: {self.assigned_hall.movie_theater} ' \
               f'Hall: {self.assigned_hall} ' \
               f'Date: {self.get_date()} ' \
               f'Time:{self.get_time()} '

    def get_date(self):
        return self.start_time.strftime('%d %B %Y')

    def get_time(self):
        return self.start_time.strftime('%I:%M')

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

    def validate_unique(self, exclude=None):
        try:
            super(PlayingTime, self).validate_unique()
        except ValidationError as e:
            raise ValidationError(f'Object with {self.assigned_hall} and {self.start_time} already exits.')


class Reservation(models.Model):
    user = models.ForeignKey(User,  null=True, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, null=True, on_delete=models.CASCADE)
    playing_time = models.ForeignKey(PlayingTime, null=True, on_delete=models.CASCADE, verbose_name='Cinema/Hall/Date')
    is_confirmed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        unique_together = ['playing_time', 'seat']


    def __str__(self):
        return f'{self.user}/ {self.seat}/'
