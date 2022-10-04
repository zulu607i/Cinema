from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from cinema import settings as base_settings
from PIL import Image
import os


# Create your models here.


class Movie(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, verbose_name='Title')
    poster = models.ImageField(verbose_name='Poster', max_length=500)
    description = models.TextField(max_length=200, null=True, verbose_name='Description', blank=True)
    imdb_id = models.CharField(max_length=30, null=True, verbose_name='IMDB_id')
    length_min = models.IntegerField(verbose_name='Length')
    trailer_url = models.URLField(max_length=200, null=True, blank=True)
    is_scheduled = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)
        self.__first_poster = self.poster

    def __str__(self):
        return self.name

    @cached_property
    def get_imdb_url(self):
        return f'{base_settings.IMDB_URL}{self.imdb_id}'

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        try:
            super(Movie, self).save(force_update=True, *args, **kwargs)
            for size_name, size in base_settings.POSTER_SIZES.items():
                img = Image.open(self.poster.path)
                image_name, image_extension = os.path.splitext(self.poster.path)
                img.thumbnail(size)
                custom_path = f'{image_name}_{size[0]}{image_extension}'
                img.save(custom_path)

        except IOError:
            print("Cannot create thumbnail for", self.poster.name)