from django.contrib import admin
from .models import *
# Register your models here.


class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'show_seats_pk']

    def show_seats_pk(self, obj):
        return ", ".join([str(a.pk) for a in obj.seats.all()])


class AdminMovieTheater(admin.ModelAdmin):
    list_display = ['name', 'show_halls']

    def show_halls(self, obj):
        return ", ".join([a.name for a in obj.halls.all()])

class AdminSeat(admin.ModelAdmin):
    list_display = ['pk', 'seat_row','seat_nr']


admin.site.register(Seat, AdminSeat)
admin.site.register(Hall, HallAdmin)
admin.site.register(MovieTheater,AdminMovieTheater)