from django import forms
from .models import Plato, Encuesta
from django.core.exceptions import ValidationError

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'disponible', 'imagen']

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['rating', 'comentario']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("La calificación debe estar entre 1 y 5.")
        return rating