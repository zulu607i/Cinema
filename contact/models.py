from django.db import models
from cinemas.models import MovieTheater
# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Full name')
    email = models.EmailField(max_length=100, verbose_name='Email')
    phone_number = models.CharField(max_length=100, verbose_name='Phone number')
    city = models.CharField(max_length=100, verbose_name='City')
    cinema = models.ForeignKey(MovieTheater, null=True, on_delete=models.CASCADE, verbose_name='Cinema')
    subject = models.CharField(max_length=100, verbose_name='Subject')
    message = models.TextField(max_length=300, verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Contacted by {self.name}'