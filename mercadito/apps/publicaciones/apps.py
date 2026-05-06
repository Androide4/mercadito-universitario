from django.apps import AppConfig

class PublicacionesConfig(AppConfig):
    DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = "apps.publicaciones"