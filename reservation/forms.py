from django import forms
from .models import Reservation
from movies.models import Movie


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['seat', 'movie_theater']
        unique_together = (
            ['user', 'seat']
        )
