from django.core.mail import send_mail
from django.shortcuts import render, redirect
from movies.models import Movie
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from cinema.settings import EMAIL_HOST_USER, EMAIL_HOST
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
            contact.subject, email_message, EMAIL_HOST, [EMAIL_HOST_USER]
        )
        return redirect('home')

    return render(request, 'contact_form.html', {'form': form})


