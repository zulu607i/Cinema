import requests
from pathlib import Path
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
            csv_file = TextIOWrapper(request.FILES['csv_file'], encoding='utf-8')
            movies = csv.DictReader(csv_file)
            added_movies = []
            updated_movies = []
            system_list = Movie.objects.values_list('pk', flat=True)
            for movie in movies:
                created_movie = Movie(**movie)
                try:
                    # name = movie["poster"].split("/")[-1]
                    # response = requests.get(created_movie.poster)

                    # if response.status_code == 200:
                    #     created_movie.poster.save(
                    #         name, ContentFile(response.content), save=False
                    #     )
                    if int(movie['pk']) not in system_list:
                        added_movies.append(Movie(**movie))
                    elif int(movie['pk']) in system_list:
                        updated_movies.append(Movie(**movie))
                except (requests.exceptions.MissingSchema, IntegrityError) as e:
                    messages.error(
                        request=request,
                        message=f"\nFailed to add movie: {movie} to the DB due to following error: {e}",
                    )

            Movie.objects.bulk_create(added_movies)
            Movie.objects.bulk_update(updated_movies,
                                      fields=['name', 'poster', 'description', 'imdb_id', 'length_min',
                                              'trailer_url'])

            return redirect("admin:movies_movie_changelist")

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