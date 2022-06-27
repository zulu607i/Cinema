import csv
import requests
from pathlib import Path
from django.contrib import admin
from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.urls import path, reverse
from .models import Movie
from django.forms import *
from django.contrib import messages
from io import TextIOWrapper
from zipfile import ZipFile
from cinema.settings import MEDIA_ROOT

# Register your models here.


class CsvForm(forms.Form):
    csv_file = forms.FileField()


class ZipFileForm(forms.Form):
    zip_file = forms.FileField()


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    change_list_template = "movies/movie_admin.html"

    def get_urls(self):
        urls = super().get_urls()
        defined_urls = [
            path("import_csv/", self.import_movies),
            path("import_zip/", self.import_movies_from_zip),
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

    def import_movies_from_zip(self, request):
        form = ZipFileForm(request.POST, request.FILES)
        if form.is_valid():
            zip_file = ZipFile(request.FILES['zip_file'])
            files = zip_file.namelist()
            for csv_file in files:
                path = MEDIA_ROOT

                if csv_file.endswith('.csv'):
                    zip_file.extractall(path=path)
                    with open(f'{path}/{csv_file}', 'r') as csv_file:
                        csv_data = csv.DictReader(csv_file)
                        added_movies = []
                        updated_movies = []
                        system_list = Movie.objects.values_list('pk', flat=True)
                        for movie_data in csv_data:
                            try:
                                created_movie = Movie(**movie_data)
                                poster_path = Path(path + movie_data['poster'])
                                created_movie.poster = poster_path.name
                                if int(movie_data['pk']) not in system_list:
                                    added_movies.append(created_movie)
                                elif int(movie_data['pk']) in system_list:
                                    updated_movies.append(created_movie)
                            except (requests.exceptions.MissingSchema, IntegrityError) as e:
                                messages.error(
                                    request=request,
                                    message=f"\nFailed to add movie: {created_movie} to the DB due to following error: {e}",
                                )

                        Movie.objects.bulk_create(added_movies)
                        Movie.objects.bulk_update(updated_movies,
                                                  fields=['name', 'poster', 'description', 'imdb_id', 'length_min',
                                                          'trailer_url'])
                return redirect('admin:movies_movie_changelist')

        return render(request, 'movies/import_movies.html', {'form': form})