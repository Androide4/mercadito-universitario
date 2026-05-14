# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("apps.accounts.urls")),
    path('admin/', admin.site.urls),
    path('publicaciones/', include('apps.publicaciones.urls')),
    path('interacciones/', include('apps.interacciones.urls')),
    path('solicitudes/', include('apps.solicitudes.urls')),
    path('accounts/', include('apps.accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)