from django.db import models

# Create your models here.
from django.db import models


class Usuario(models.Model):
    class RolChoices(models.TextChoices):
        ESTUDIANTE = "estudiante", "Estudiante"
        ADMIN = "admin", "Admin"

    class EstadoChoices(models.TextChoices):
        ACTIVO = "activo", "Activo"
        INACTIVO = "inactivo", "Inactivo"

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    carrera = models.CharField(max_length=120)
    semestre = models.PositiveSmallIntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    foto_perfil = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    rol = models.CharField(
        max_length=20,
        choices=RolChoices.choices,
        default=RolChoices.ESTUDIANTE
    )
    estado = models.CharField(
        max_length=20,
        choices=EstadoChoices.choices,
        default=EstadoChoices.ACTIVO
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_sesion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.correo}"