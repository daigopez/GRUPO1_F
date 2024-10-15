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


# modificación de los datos del usuario registrado:

class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Nueva contraseña')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Incluye la contraseña

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Comprobar si el nombre de usuario ya existe en la base de datos
        if User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise ValidationError("No se puede cambiar a ese nombre de usuario porque ya está ocupado.")
        return username

#Control de modifcacion de usuario si ya existe

