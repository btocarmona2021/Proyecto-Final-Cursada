# Importo urls y include para definir rutas, y DefaultRouter para generar automáticamente las rutas CRUD de los ViewSets.
from django.urls import path, include

# importo DefaultRouter para generar automáticamente las rutas CRUD de los ViewSets.
from rest_framework.routers import DefaultRouter

# importo las vistas de Turno y Servicio para registrarlas en el router.
from .views import TurnoViewSet, ServicioViewSet

router = DefaultRouter()
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'servicios', ServicioViewSet, basename='servicio')

urlpatterns = [
    path('', include(router.urls)),
]
