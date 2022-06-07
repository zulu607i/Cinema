from django.core.mail import send_mail
from django.shortcuts import render, redirect
from movies.models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from cinema.settings import EMAIL_HOST_USER
from ratelimit.decorators import ratelimit
# Create your views here.


@ratelimit(key="ip", rate="30/m", block=True)
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


@ratelimit(key="ip", rate="30/m", block=True)
def contact_form(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data('email')
            subject = form.cleaned_data('subject')
            message = form.cleaned_data('message')
            send_mail(
                subject, message, email, EMAIL_HOST_USER
            )
            return redirect('home')

    return render(request, 'contact_form.html', {'form': form})


