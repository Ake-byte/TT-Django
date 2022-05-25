from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Registro(models.Model):

    def __str__(self):
        return self.nombre_registro

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    nombre_registro = models.CharField(max_length=200)
    descripcion_registro = models.CharField(max_length=200)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    archivo_registro = models.FileField()
    
