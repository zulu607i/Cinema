from django.contrib import admin
from .models import *
# Register your models here.


class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'movie_theater']




class AdminSeat(admin.ModelAdmin):
    list_display = ['pk', 'seat_row', 'seat_nr', 'halls']


admin.site.register(Seat, AdminSeat)
admin.site.register(Hall, HallAdmin)
admin.site.register(MovieTheater)