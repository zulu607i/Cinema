from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from reservation.models import Reservation
from .forms import ReservationForm
from movies.models import Movie
from cinema.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from cinemas.models import Hall
import csv
# Create your views here.


@login_required()
def book_a_ticket(request, pk, hall_pk):
    movie = Movie.objects.get(pk=pk)
    hall = Hall.objects.get(pk=hall_pk)
    form = ReservationForm(request.POST, movie=movie.pk, seats=hall.pk, hall=hall_pk)
    if form.is_valid():
        reservation = form.save()
        reservation.user = request.user
        reservation.movie = movie
        reservation.save()

        message = f'Hi,{reservation.user}! Your reservation with ID {reservation.pk} has been created. ' \
                  f'Movie: {reservation.movie}, on {reservation.playing_time.start_time} in' \
                  f' {reservation.playing_time.assigned_hall}, seat {reservation.seat} at {reservation.playing_time.assigned_hall.movie_theater}'

        send_mail(f'You booked a ticket for {reservation.movie}',
                  message,
                  EMAIL_HOST_USER,
                  [f'{reservation.user.email}']
                  )

        return redirect('home')

    return render(request, 'reservation/reserve.html', {'form': form,})

def get_csv_file(request, pk):
    user = User.objects.get(pk=pk)
    reservations = Reservation.objects.filter(user=request.user)

    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        response['Content=-Disposition'] = f'attachment; filename=reservation_{user.username}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'User', 'Hall', 'Movie', 'Seat', 'Start time'])
        for r in reservations:

            writer.writerow([r.pk,
                             r.user,
                             r.playing_time.assigned_hall,
                             r.playing_time.assigned_movie,
                             r.seat,
                             r.playing_time.start_time])

        return response

    return render(request, 'reservation/user_reservation.html', {'reservations': reservations})

