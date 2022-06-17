from .models import *


def expired_reservations():
    reservation = Reservation.objects.all()
    for r in reservation:
        exipired_time = r.playing_time.start_time - timedelta(minutes=30)
        print(exipired_time)
        if not r.is_confirmed:
            if r.playing_time.start_time > exipired_time:
                r.expired = True
                r.save()
                print(r.expired)
            return r