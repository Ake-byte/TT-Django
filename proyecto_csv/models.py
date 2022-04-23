from django.db import models

# Create your models here.


class Registro(models.Model):

    def __str__(self):
        return self.nombre_registro

    nombre_registro = models.CharField(max_length=200)
    descripcion_registro = models.CharField(max_length=200)
    archivo_registro = models.FileField(blank=True, null=True)
