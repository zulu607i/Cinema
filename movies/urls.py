from django.urls import path
from . import views

urlpatterns = [
    path('import_movies/', views.import_movies, name='import_movies'),
]