from django.test import TestCase
# Create your tests here.
from django.test import TestCase
from .models import *
# Create your tests here.


class SeatGenerationTest(TestCase):
    def test_gs(self):
        gs = generate_seat(2, 2)
        self.assertTrue(
            ["1A", "2A", "1B", "2B"], [seat.seat_name for seat in gs]
        )