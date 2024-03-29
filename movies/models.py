from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from cinema import settings
from cinemas.models import Hall
from datetime import timedelta

# Create your models here.


class Movie(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, verbose_name='Title')
    poster = models.URLField(verbose_name='Poster')
    description = models.TextField(max_length=200, null=True, verbose_name='Description', blank=True)
    imdb_id = models.CharField(max_length=30, null=True, verbose_name='IMDB_id')
    length_min = models.IntegerField(verbose_name='Length')
    trailer_url = models.URLField(max_length=200, null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @cached_property
    def get_imdb_url(self):
        return f'{settings.IMDB_URL}{self.imdb_id}'
