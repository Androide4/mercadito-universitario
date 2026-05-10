from django.apps import AppConfig


class InteraccionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interacciones'          # ← prefijo 'apps.' requerido por el subfolder
    verbose_name = 'Interacciones y Soporte Visual'
