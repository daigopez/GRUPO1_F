from django import forms
from .models import Plato, Encuesta, PlatoSemanal
from django.core.exceptions import ValidationError

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre', 'descripcion', 'precio', 'disponible', 'imagen']  # Agrega la imagen

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['rating', 'comentario']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("La calificación debe estar entre 1 y 5.")
        return rating

class PlatoSemanalForm(forms.ModelForm):
    class Meta:
        model = PlatoSemanal
        fields = ['dia', 'plato', 'comentario']

# Se actualiza el formulario con el nuevo campo de correo electronico

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']