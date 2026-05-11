# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Raíz del sitio → home de interacciones
    path('', include('apps.interacciones.urls')),

    # También accesible con prefijo (no eliminar, lo usan los parciales)
    path('interacciones/', include('apps.interacciones.urls')),

    # Cuando lleguen los compañeros:
    # path('accounts/', include('apps.accounts.urls')),
    # path('publicaciones/', include('apps.publicaciones.urls')),
    # path('solicitudes/', include('apps.solicitudes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)