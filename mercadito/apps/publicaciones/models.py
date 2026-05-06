from django.db import models


class Publicacion(models.Model):
    class CategoriaChoices(models.TextChoices):
        LIBROS = "libros", "Libros"
        ROPA = "ropa", "Ropa"
        UTILES = "utiles", "Útiles"
        ELECTRONICA = "electronica", "Electrónica"
        MUEBLES = "muebles", "Muebles"
        OTROS = "otros", "Otros"

    class TipoIntercambioChoices(models.TextChoices):
        INTERCAMBIO = "intercambio", "Intercambio"
        VENTA = "venta", "Venta"
        REGALO = "regalo", "Regalo"

    class EstadoArticuloChoices(models.TextChoices):
        NUEVO = "nuevo", "Nuevo"
        USADO = "usado", "Usado"
        SEMINUEVO = "seminuevo", "Seminuevo"

    class EstadoPublicacionChoices(models.TextChoices):
        ACTIVA = "activa", "Activa"
        PAUSADA = "pausada", "Pausada"
        CERRADA = "cerrada", "Cerrada"

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(
        max_length=30,
        choices=CategoriaChoices.choices
    )
    tipo_intercambio = models.CharField(
        max_length=20,
        choices=TipoIntercambioChoices.choices
    )
    precio_referencial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    estado_articulo = models.CharField(
        max_length=20,
        choices=EstadoArticuloChoices.choices,
        default=EstadoArticuloChoices.USADO
    )
    estado_publicacion = models.CharField(
        max_length=20,
        choices=EstadoPublicacionChoices.choices,
        default=EstadoPublicacionChoices.ACTIVA
    )
    imagenes = models.JSONField(default=list, blank=True)
    autor = models.JSONField(default=dict)
    ubicacion_entrega = models.CharField(max_length=150, null=True, blank=True)
    tags = models.JSONField(default=list, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo