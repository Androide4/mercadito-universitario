from django.db import models


class Favorito(models.Model):
    usuario = models.JSONField(default=dict)
    publicacion = models.JSONField(default=dict)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Favorito de {self.usuario}"


class Comentario(models.Model):
    class EstadoComentarioChoices(models.TextChoices):
        VISIBLE = "visible", "Visible"
        OCULTO = "oculto", "Oculto"

    publicacion = models.JSONField(default=dict)
    usuario = models.JSONField(default=dict)
    texto = models.CharField(max_length=300)
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=EstadoComentarioChoices.choices,
        default=EstadoComentarioChoices.VISIBLE
    )

    def __str__(self):
        return self.texto[:30]