from django.db import IntegrityError
from django.shortcuts import render
import requests
from movies.models import Movie
from .forms import *
from django.contrib.admin.views.decorators import staff_member_required
import csv
from django.contrib import messages

# Create your views here.

@staff_member_required
def import_movies(request):
    form = CsvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        form = CsvForm()
        obj = Csv.objects.get(is_used=False)
        with open(obj.csv.path, 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                try:
                    if i == 0:
                        pass
                    else:
                        Movie.objects.create(
                            name=row[0],
                            poster=row[1],
                            description=row[2],
                            imdb_id=row[3],
                            length_min=int(row[4]),
                            trailer_url=row[5]
                        )
                    obj.is_used = True
                    obj.save()
                except (requests.exceptions.MissingSchema, IntegrityError) as e:
                    messages.error(
                        request=request,
                        message=f"\nFailed to add movie: {row[0]} to the DB due to following error: {e}",
                    )

    return render(request, 'movies/import_movies.html', {'form': form})