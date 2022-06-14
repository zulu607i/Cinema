from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:pk>/<int:hall_pk>', views.book_a_ticket, name='reserve'),
    path('csv/<int:pk>', views.get_csv_file, name='get_csv'),
]