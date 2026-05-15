# historia_clinica/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultaClinicaViewSet, RecetaItemViewSet, VacunaViewSet

router = DefaultRouter()
router.register(r'consultas', ConsultaClinicaViewSet, basename='consulta')
router.register(r'recetas', RecetaItemViewSet, basename='receta')
router.register(r'vacunas', VacunaViewSet, basename='vacuna')

urlpatterns = [
    path('', include(router.urls)),
]