from django.db import models
from django.contrib.auth.models import User
from cinema import settings

# Create your models here.


class Movie(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, verbose_name='Title')
    poster = models.ImageField(upload_to='images/', verbose_name='Poster')
    description = models.TextField(max_length=200, null=True, verbose_name='Description')
    imdb_id = models.CharField(max_length=30, null=True, unique=True, verbose_name='IMDB_id')
    length_min = models.IntegerField(verbose_name='Lenght')
    is_scheduled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_imbd_url(self):
        return f'{settings.IMDB_URL}{self.imdb_id}'






