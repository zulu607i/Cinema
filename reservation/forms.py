from django import forms

# Not used anymore!
# class ReservationForm(forms.ModelForm):
#     def __init__(self, *args, movie=None, seats=None, hall=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['playing_time'].queryset = PlayingTime.objects.filter(assigned_movie=movie, assigned_hall=hall)
#         self.fields['seat'].queryset = Seat.objects.filter(halls=seats)
#
#     class Meta:
#         model = Reservation
#         fields = ['seat', 'playing_time']
#         unique_together = (
#             ['playing_time', 'user']
#         )
