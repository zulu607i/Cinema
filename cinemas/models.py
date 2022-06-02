from django.db import models
from locations.models import County, City, Street
# Create your models here.


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

    def __str__(self):
        return self.name


class Seat(models.Model):
    seat_nr = models.CharField(max_length=10, unique=True)
    seat_row = models.CharField(max_length=10, default='')
    is_reserved = models.BooleanField(default=False)
    halls = models.ForeignKey(Hall, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.seat_row} {self.seat_nr}'




