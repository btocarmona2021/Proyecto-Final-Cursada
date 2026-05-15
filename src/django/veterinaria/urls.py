from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('usuarios.urls')),
    path('api/', include('agenda.urls')),
    path('api/', include('clinica.urls')),
    path('api/', include('historia_clinica.urls')),
    path('api/', include('internaciones.urls')),
    path('api/', include('mascotas.urls')),
    path('api/', include('notificaciones.urls')),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)