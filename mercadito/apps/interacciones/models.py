from django.db import models
class Favorito(models.Model):
   
    usuario = models.JSONField(default=dict)
    publicacion = models.JSONField(default=dict)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-fecha_agregado']
        verbose_name = "Favorito"
        verbose_name_plural = "Favoritos"
    def __str__(self):
        nombre = self.usuario.get('nombre', 'Desconocido')
        titulo = self.publicacion.get('titulo', 'Sin título')
        return f"Favorito de {nombre} → {titulo}"
    
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
    class Meta:
        ordering = ['-fecha_comentario']
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
    def __str__(self):
        return self.texto[:30]