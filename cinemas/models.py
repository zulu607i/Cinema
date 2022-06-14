from django.db import models
from locations.models import County, City, Street
# Create your models here.


class MovieTheater(models.Model):
    name = models.CharField(max_length=200, unique=True)
    county = models.ForeignKey(County, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, on_delete=models.SET_NULL)
    street = models.ForeignKey(Street, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Hall(models.Model):
    name = models.CharField(max_length=200, blank=False)
    movie_theater = models.ForeignKey(MovieTheater, null=True, on_delete=models.SET_NULL)
    rows = models.IntegerField(default=15)
    seats_per_row = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Seat(models.Model):
    seat_name = models.CharField(default='A1', max_length=4)
    halls = models.ForeignKey(Hall, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.seat_name} {self.halls.name}'


def generate_seat(rows, seats_per_row):
    seats = []
    for row in range(0, rows):
        for l in range(1, seats_per_row):
            seat = Seat(seat_name=str(l) + (chr(65 + row)))
            seats.append(seat)

    return seats
