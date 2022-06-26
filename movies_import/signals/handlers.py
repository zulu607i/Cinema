from django.db.models.signals import post_save
from django.dispatch import receiver
from movies_import.utils import import_movies_from_zip
from movies_import.models import *


@receiver(post_save, sender=MoviesImport)
def process_zip_file(instance, **kwargs):
    import_movies_from_zip(instance.file, instance.name)