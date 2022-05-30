from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class PermisoUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    tipoPermiso = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(3), MinValueValidator(1)])

    def __str__(self):
        return self.user.username