from django.db.models.signals import post_save
from django.dispatch import receiver
from cinemas.models import generate_seat, Seat, Hall

@receiver(post_save, sender=Hall)
def hall_creation_handler(instance, **kwargs):
    gs = generate_seat(instance.rows, instance.seats_per_row)
    instance.seats.add(*gs, bulk=False)