from django.urls import path

from reservation.views import CreateCheckoutSessionView, ReservationLandingPageView, SuccessPaidView
from . import views

urlpatterns = [
    path('csv/', views.get_csv_file, name='get_csv'),
    path('booking/select-cinema/', views.select_cinema, name='select_cinema'),
    path("booking/select-movie/<int:cinema_pk>", views.select_movie, name="select_movie"),
    path("booking/select-time/<int:movie_pk>/<int:cinema_pk>", views.select_playing_time, name="select_playing_time"),
    path("booking/select-seats/<int:pk>/", views.select_seats, name="select_seats"),
    path("booking/confirm-reservation/<slug:uidb64>/", views.confirm_reservations, name="confirm_reservations"),
    path("create-checkout-session/<int:pk>", CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path("landing/", ReservationLandingPageView.as_view(), name='landing'),
    path("successfully-paid/<slug:uidb64>", SuccessPaidView.as_view(), name='success'),
]
