import os

import requests
from django.contrib import messages
from django.core.exceptions import ValidationError
from zipfile import ZipFile
from django.db import IntegrityError
from cinema.settings import MEDIA_ROOT
import csv
from pathlib import Path
from django.core.files import File
from movies.models import Movie


def validate_zipfile(zip_file):
    ext = os.path.splitext(zip_file.name)[1]
    valid_ext = ['.zip', '.rar']
    if not ext.lower() in valid_ext:
        raise ValidationError('Unsupported file extension')


def get_movies_form_zip(file, path):
    zip_file = ZipFile(file)
    files = zip_file.namelist()
    for f in files:
        if f.endswith('.csv'):
            zip_file.extractall(path=path)
            return f


def import_movies_from_zip(file, name):
    path = f'{MEDIA_ROOT}'
    csv_file = get_movies_form_zip(file, path)
    with open(f"{path}\{csv_file}", 'r') as f:
        data = csv.DictReader(f)
        added_movies = []
        system_list = Movie.objects.values_list('pk', flat=True)
        for m in data:
            created_movie = Movie(**m)
            poster_path = Path(path+m['poster'])
            created_movie.poster = poster_path.name
            print(poster_path)
            if int(m['pk']) not in system_list:
                added_movies.append(created_movie)
            elif int(m['pk']) in system_list:
                Movie.objects.bulk_update([created_movie],
                                      fields=['name', 'poster', 'description', 'imdb_id', 'length_min',
                                              'trailer_url'])

        Movie.objects.bulk_create(added_movies)






