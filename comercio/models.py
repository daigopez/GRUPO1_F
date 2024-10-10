from django.db import models
from django.contrib.auth.models import User

class Plato(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"  # Formato con dos decimales

class Encuesta(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='encuestas')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 a 5 estrellas
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'Encuesta para {self.plato.nombre} - Rating: {self.rating}'

class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato, through='ItemCarrito')

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('carrito', 'plato')  # Asegura que un plato no se repita en el carrito

class PlatoSemanal(models.Model):
    DIA_SEMANA_CHOICES = [
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo'),
    ]
    dia = models.CharField(max_length=9, choices=DIA_SEMANA_CHOICES)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.dia}: {self.plato.nombre}"

class Voto(models.Model):
    plato_semanal = models.ForeignKey(PlatoSemanal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Voto de {self.user.username} para {self.plato_semanal.plato.nombre} en {self.plato_semanal.dia}'