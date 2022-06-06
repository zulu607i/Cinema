from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import ReservationForm
from movies.models import Movie
from cinema.settings import EMAIL_HOST
from django.contrib.auth.decorators import login_required
from cinemas.models import Seat
# Create your views here.

@login_required()
def book_a_ticket(request, pk):
    movie = Movie.objects.get(pk=pk)
    form = ReservationForm(request.POST)
    if form.is_valid():
        reservation = form.save()
        reservation.user = request.user
        reservation.movie = movie
        reservation.date = movie.date_scheduled_at
        reservation.hour = movie.time_scheduled_at
        seat_object = Seat.objects.get(pk=reservation.seat.pk)
        seat_object.is_reserved = True
        reservation.save()
        seat_object.save()

        message = f'Hi,{reservation.user}! Your reservation with ID {reservation.pk} has been created. ' \
                  f'Movie: {reservation.movie}, on {reservation.date} at {reservation.hour} in {movie.hall_is_playing}, seat {reservation.seat}'
        send_mail(f'You booked a ticket for {reservation.movie}',
                  message,
                  EMAIL_HOST,
                  [f'{reservation.user.email}']
                  )

        return redirect('home')

    return render(request, 'reservation/reserve.html', {'form': form})

