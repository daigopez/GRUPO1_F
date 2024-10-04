from django.db import models

class Plato(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='platos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio:.2f}"  # Formato con dos decimales

class Encuesta(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='encuestas')  # Agregar related_name
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1 a 5 estrellas
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'Encuesta para {self.plato.nombre} - Rating: {self.rating}'