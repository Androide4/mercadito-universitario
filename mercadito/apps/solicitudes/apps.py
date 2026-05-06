from django.apps import AppConfig

class SolicitudesConfig(AppConfig):
    DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = "apps.solicitudes"