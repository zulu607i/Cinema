from base64 import urlsafe_b64decode
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode
from api.utils import get_current_week
from reservation.models import Reservation, PlayingTime
from cinema.settings import EMAIL_HOST_USER
from django.contrib.auth.decorators import login_required
from cinemas.models import Hall, MovieTheater, Seat
import csv
from ratelimit.decorators import ratelimit
# Create your views here.

@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def get_csv_file(request):
    reservations = Reservation.objects.filter(user=request.user)
    if request.method == "POST":
        response = HttpResponse(content_type='text/csv')
        filename = f'{request.user}-reservations'
        response['Content=-Disposition'] = f'attachment; filename={filename}.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'User', 'Hall', 'Movie', 'Seat', 'Start time'])
        for r in reservations:
            if r.is_confirmed:
                writer.writerow([r.pk,
                                 r.user,
                                 r.playing_time.assigned_hall,
                                 r.playing_time.assigned_movie,
                                 r.seat,
                                 r.playing_time.start_time,
                                 r.is_confirmed,
                                 ])

        return response

    return render(request, 'reservation/user_reservation.html', {'reservations': reservations})


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_cinema(request):
    cinemas = MovieTheater.objects.all()
    return render(request, 'reservation/select_cinema.html', {'cinemas': cinemas})


def select_movie(request, cinema_pk):
    if request.method == "GET":
        movies_playing_time = PlayingTime.objects.filter(assigned_hall__in=Hall.objects.filter(
            movie_theater=cinema_pk),
            start_time__range=get_current_week()).distinct('assigned_movie')

        if movies_playing_time:
            movies = [pt.assigned_movie for pt in movies_playing_time]  # (pt -> playing_time)
        else:
            movies = []

        return render(request, 'reservation/select_movie.html', {'movies': movies})
    if request.method == "POST":
        movie_pk = request.POST['movie_pk']
        return redirect('select_playing_time', movie_pk=movie_pk, cinema_pk=cinema_pk)

@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_playing_time(request, movie_pk, cinema_pk):
    if request.method == "GET":
        playing_times = PlayingTime.objects.filter(
            assigned_movie=movie_pk,
            assigned_hall__in=Hall.objects.filter(movie_theater=cinema_pk),
        )
        return render(
            request, "reservation/select_playing_time.html", {"playing_times": playing_times}
        )

@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def select_seats(request, pk):
    playing_time = PlayingTime.objects.get(pk=pk)
    if request.method == "GET":
        reserved_seats = Reservation.objects.filter(
            playing_time_id=pk
        ).values_list('seat__seat_name', flat=True)
        seats = Seat.objects.filter(halls=playing_time.assigned_hall.id).order_by('seat_name')
        return render(
            request,
            "reservation/select_seats.html",
            {
                "reserved_seats": reserved_seats,
                "seats": seats,
            },
        )

    if request.method == "POST":
        seats = request.POST.getlist("seats")
        user = User.objects.get(username=request.user)
        reservations = []
        for seat in seats:
            reservations.append(
                Reservation(
                    seat_id=seat,
                    user=user,
                    playing_time=playing_time,
                )
            )
        try:
            existing_ids = list(
                Reservation.objects.filter(
                    playing_time=playing_time, user=user
                ).values_list("id", flat=True)
            )
            Reservation.objects.bulk_create(reservations)

        except IntegrityError:
            messages.success(request, f"Seat {seats} is already reserved")
            return redirect(request.path)

        new_ids = list(
            Reservation.objects.exclude(id__in=existing_ids).values_list(
                "id", flat=True
            ).filter(user=user, playing_time=playing_time)
        )
        ids_string = ",".join([str(res_id) for res_id in new_ids])
        encoded_ids = urlsafe_base64_encode(force_bytes(ids_string))
        email_subject = f"Your booking for: {playing_time.assigned_movie.name} was completed successfully"
        current_site = get_current_site(request)
        seats_names = " ".join(seats)
        email_message = render_to_string(
            "reservation/booking_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": encoded_ids,
                "seats": seats_names,
                "hall_name": playing_time.assigned_hall.name,
                "movie_name": playing_time.assigned_movie.name,
            },
        )

        send_mail(
            email_subject,
            email_message,
            EMAIL_HOST_USER,
            [user.email],
        )
        return redirect("home")


@login_required()
@ratelimit(key="ip", rate="30/m", block=True)
def confirm_reservations(request, uidb64):
    uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
    ids = force_str(urlsafe_b64decode(uidb64_padded)).split(",")
    Reservation.objects.filter(id__in=ids).update(is_confirmed=True)
    return HttpResponse("Thank you for confirming your reservations")

