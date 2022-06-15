from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('contact/', views.contact_form, name='contact_form'),
    path('details/<int:pk>/', views.MovieDetailView.as_view(), name='movie_details'),
]