import requests
from django.contrib import admin
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.urls import path
from .models import Movie
from django.forms import *
import csv
from django.contrib import messages
from io import TextIOWrapper

# Register your models here.


class CsvForm(forms.Form):
    csv_file = forms.FileField()


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    change_list_template = "movies/movie_admin.html"

    def get_urls(self):
        urls = super().get_urls()
        defined_urls = [
            path("import_csv/", self.import_movies),
        ]
        return defined_urls + urls

    def import_movies(self, request):
        form = CsvForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'], encoding=request.encoding)
            movies = csv.reader(csv_file)
            for movie in movies:
                try:
                    Movie.objects.create(name=movie[0],
                                         poster=movie[1],
                                         description=movie[2],
                                         imdb_id=movie[3],
                                         length_min=int(movie[4]),
                                         trailer_url=movie[5])

                except (requests.exceptions.MissingSchema, IntegrityError) as e:
                    messages.error(
                        request=request,
                        message=f"\nFailed to add movie: {movie[0]} to the DB due to following error: {e}",
                    )

        return render(request, 'movies/import_movies.html', {'form': form})
