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
    thumbnail = models.ImageField(upload_to='thumbnails', max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name

    @cached_property
    def get_imdb_url(self):
        return f'{base_settings.IMDB_URL}{self.imdb_id}'

    def create_thumbnail(self, size=(128, 128)):

        if not self.poster:
            return

        poster_type = self.poster.file.content_type

        if poster_type == 'image/jpeg':
            pillow_type = 'jpeg'
            extension = 'jpg'

        if poster_type == 'image/png':
            pillow_type = 'png'
            extension = 'png'

        try:
            poster = Image.open(io.BytesIO(self.poster.read()))
            poster.thumbnail(size, Image.ANTIALIAS)
            temp_handle = io.BytesIO()
            poster.save(temp_handle, pillow_type)
            temp_handle.seek(0)

            uploaded_file = SimpleUploadedFile(os.path.split(self.poster.name)[-1],
                                     temp_handle.read(), content_type=poster_type)
            self.thumbnail.save(
                '{0}_thumbnail.{1}'.format(os.path.splitext(uploaded_file.name)[0], extension),
                uploaded_file,
                save=False)
        except IOError:
            print("Cannot create thumbnail for", self.poster.name)

    def save(self, *args, **kwargs):
        self.create_thumbnail()
        force_update = False

        if self.id:
            force_update = True
        super(Movie, self).save(force_update=force_update)