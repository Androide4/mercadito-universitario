from django.apps import AppConfig


class InteraccionesConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'apps.interacciones'          # ← prefijo 'apps.' requerido por el subfolder
    verbose_name = 'Interacciones y Soporte Visual'
