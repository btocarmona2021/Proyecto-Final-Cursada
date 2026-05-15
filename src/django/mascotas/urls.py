# mascotas/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MascotaViewSet, EspecieViewSet, RazaViewSet

router = DefaultRouter()
router.register(r'mascotas', MascotaViewSet, basename='mascota')
router.register(r'especies', EspecieViewSet, basename='especie')
router.register(r'razas', RazaViewSet, basename='raza')

urlpatterns = [
    path('', include(router.urls)),
]