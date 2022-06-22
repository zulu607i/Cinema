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
            movies = csv.DictReader(csv_file)
            movies_list = []
            for movie in movies:
                try:
                    created_movie = Movie(**movie)
                    name = movie["poster"].split("/")[-1]
                    response = requests.get(created_movie.poster)
                    if response.status_code == 200:
                        created_movie.poster.save(
                            name, ContentFile(response.content), save=False
                        )

                except (requests.exceptions.MissingSchema, IntegrityError) as e:
                    messages.error(
                        request=request,
                        message=f"\nFailed to add movie: {movie} to the DB due to following error: {e}",
                    )
                else:
                    movies_all = Movie.objects.all()
                    for m in movies_all:
                        if not m.pk:
                            movies_list.append(created_movie)
                            Movie.objects.bulk_create(movies_list)
                        else:
                            movies_list.append(created_movie)
                            Movie.objects.bulk_update(movies_list, fields=['name', 'poster', 'description', 'imdb_id', 'length_min', 'trailer_url'])

                    return redirect("..")

        return render(request, 'movies/import_movies.html', {'form': form})
