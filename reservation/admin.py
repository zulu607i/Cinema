from django.contrib import admin
from .models import Reservation, PlayingTime
# Register your models here.

admin.site.register(Reservation)
admin.site.register(PlayingTime)