from .models import Csv
from django import forms


class CsvForm(forms.ModelForm):
    class Meta:
        model = Csv
        fields = ['csv']