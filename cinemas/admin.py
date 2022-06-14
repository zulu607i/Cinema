from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import *
from nested_inline.admin import NestedTabularInline, NestedModelAdmin
from django import forms

# Register your models here.

class SeatInline(NestedTabularInline):
    model = Seat
    extra = 0


class HallInline(NestedTabularInline):
    model = Hall
    extra = 0
    inlines = (SeatInline,)



@admin.register(MovieTheater)
class CinemaAdmin(NestedModelAdmin):
    inlines = (HallInline,)


@admin.register(Hall)
class HallAdmin(NestedModelAdmin):
    inlines = (SeatInline,)



admin.site.register(Seat)