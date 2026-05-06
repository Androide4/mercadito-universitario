from django.apps import AppConfig

class AccountsConfig(AppConfig):
    DEFAULT_AUTO_FIELD = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = "apps.accounts"