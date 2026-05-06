from django.db import models


class SolicitudIntercambio(models.Model):
    class EstadoSolicitudChoices(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        ACEPTADA = "aceptada", "Aceptada"
        RECHAZADA = "rechazada", "Rechazada"
        CANCELADA = "cancelada", "Cancelada"

    publicacion = models.JSONField(default=dict)
    solicitante = models.JSONField(default=dict)
    mensaje = models.TextField()
    propuesta_intercambio = models.TextField(null=True, blank=True)
    estado_solicitud = models.CharField(
        max_length=20,
        choices=EstadoSolicitudChoices.choices,
        default=EstadoSolicitudChoices.PENDIENTE
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    respuesta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Solicitud - {self.estado_solicitud}"