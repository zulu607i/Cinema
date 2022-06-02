from django.shortcuts import render
from movies.models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def homepage(request):
    movies = Movie.objects.filter(is_scheduled=True)
    paginator = Paginator(movies, 4)
    page = request.GET.get("page", 1)
    try:
        movies_paginated = paginator.get_page(page)
    except PageNotAnInteger:
        movies_paginated = paginator.page(1)
    except EmptyPage:
        movies_paginated = paginator.page(paginator.num_pages)
    return render(request, "base.html", {"movies": movies_paginated})