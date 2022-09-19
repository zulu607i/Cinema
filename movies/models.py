from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
from cinema import settings as base_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
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

    def __str__(self):
        return self.name

    @cached_property
    def get_imdb_url(self):
        return f'{base_settings.IMDB_URL}{self.imdb_id}'

    def save(self, *args, **kwargs):
        super(Movie, self).save(*args, **kwargs)
        img = Image.open(self.poster.path)
        output_size_small = base_settings.POSTER_SIZES['small']
        output_size_large = base_settings.POSTER_SIZES['large']
        output_size_medium = base_settings.POSTER_SIZES['medium']
        image_name, image_extension = os.path.splitext(self.poster.path)

        """ Large image """
        img.thumbnail(output_size_large)
        custom_path_large = f'{image_name}_{output_size_large[0]}{image_extension}'
        img.save(custom_path_large)

        """ Medium Image"""
        img.thumbnail(output_size_medium)
        custom_path_medium = f'{image_name}_{output_size_medium[0]}{image_extension}'
        img.save(custom_path_medium)

        """Small Image """
        img.thumbnail(output_size_small)
        custom_path_small = f'{image_name}_{output_size_small[0]}{image_extension}'
        img.save(custom_path_small)