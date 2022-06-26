from django.db import models

# Create your models here.

class MoviesImport(models.Model):
    file = models.FileField(upload_to='zipped_files')
    name = models.CharField(max_length=35, blank=True)

    def __str__(self):
        return self.file.name
