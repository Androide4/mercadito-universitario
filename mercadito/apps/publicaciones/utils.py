from django.core.files.storage import FileSystemStorage
from django.conf import settings

def guardar_imagen(archivo):
    storage = FileSystemStorage(
        location=settings.MEDIA_ROOT,
        base_url=settings.MEDIA_URL
    )

    nombre = storage.save(archivo.name, archivo)
    return storage.url(nombre)