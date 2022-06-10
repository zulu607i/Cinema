from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:pk>/<int:hall_pk>', views.book_a_ticket, name='reserve'),
]