from django.urls import path
from . import views

urlpatterns = [
    path('reserve/<int:pk>', views.book_a_ticket, name='reserve'),
]