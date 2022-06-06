from django import forms
from .models import Reservation
from movies.models import Movie


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['seat', 'playing_time']
        unique_together = (
            ['user', 'seat']
        )
