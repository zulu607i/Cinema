from django.apps import AppConfig


class MoviesImportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_import'

    def ready(self):
        from movies_import.signals import handlers