import django_filters
from .models import PlayingTime
from cinemas.models import *


class PlayingTimeFilter(django_filters.FilterSet):
    movie = django_filters.ChoiceFilter(method='title_filter', label='Assigned product', empty_label='')

    class Meta:
        model = PlayingTime
        fields = ['assigned_movie', 'assigned_hall']

    def title_filter(self, queryset, name, value):
        return queryset.filter(assigned_movie__icontains=value)