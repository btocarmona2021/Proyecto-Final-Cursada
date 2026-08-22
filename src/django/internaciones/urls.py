from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InternacionViewSet, EvolucionInternacionViewSet

router = DefaultRouter()
router.register(r'internaciones', InternacionViewSet, basename='internacion')
router.register(r'evoluciones-internacion', EvolucionInternacionViewSet, basename='evolucion-internacion')

urlpatterns = [
    path('', include(router.urls)),
]