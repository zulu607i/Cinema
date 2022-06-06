from django.contrib import admin
from .models import Reservation
# Register your models here.


class AdminReservation(admin.ModelAdmin):
    list_display = ['pk', 'user', 'seat', 'movie',]


admin.site.register(Reservation, AdminReservation)