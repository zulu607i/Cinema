from django.db.models import F
from django.utils import timezone

from .models import *


def expired_reservations():
    time_now = timezone.now()
    reservations = Reservation.objects.select_related('playing_time').annotate(
        expired_time=F('playing_time__start_time') - time_now).filter(
        expired_time__lte=timedelta(minutes=30))
    reservations.filter(is_confirmed=False).update(expired=True)


