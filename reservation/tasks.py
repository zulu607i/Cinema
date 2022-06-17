from .models import *


def expired_reservations():
    reservation = Reservation.objects.all()
    for r in reservation:
        expired_time = r.playing_time.start_time - timedelta(minutes=30)

        if not r.is_confirmed:
            if r.playing_time.start_time > expired_time:
                r.expired = True
                r.save()

            return r
