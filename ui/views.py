from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from api.utils import get_current_week, get_next_week
from movies.models import Movie
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from cinema.settings import EMAIL_HOST_USER, EMAIL_HOST, EMAIL_HOST_PASSWORD
from cinema.settings import EMAIL_HOST_USER
from ratelimit.decorators import ratelimit
# Create your views here.


@ratelimit(key="ip", rate="30/m", block=True)
def homepage(request):
    playing_movies_this_week = Movie.objects.filter(playingtime__start_time__range=get_current_week())

    playing_movies_next_week = Movie.objects.filter(playingtime__start_time__range=get_next_week())

    # paginator = Paginator(playing_movies_this_week, 10)
    # page = request.GET.get("page", 1)
    #
    # try:
    #     movies_paginated = paginator.get_page(page)
    # except PageNotAnInteger:
    #     movies_paginated = paginator.page(1)
    # except EmptyPage:
    #     movies_paginated = paginator.page(paginator.num_pages)

    return render(request, "homepage/home_content.html",
                  {"movies": playing_movies_this_week,
                   "playing_movies_next_week": playing_movies_next_week,
                   })


@ratelimit(key="ip", rate="30/m", block=True)
def contact_form(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save()

        email_message = f'Name: {contact.name} \n ' \
                        f'Phone: {contact.phone_number} \n ' \
                        f'Email: {contact.email} \n' \
                        f'City: {contact.city}\n' \
                        f'Cinema: {contact.cinema} \n' \
                        f'Message: {contact.message}'
        send_mail(
            contact.subject,
            email_message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[EMAIL_HOST_USER],
            auth_user=EMAIL_HOST_USER,
            auth_password=EMAIL_HOST_PASSWORD,
        )
        return redirect('home')

    return render(request, 'contact_form.html', {'form': form})


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/details.html'
