# clinica/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VeterinariaViewSet

router = DefaultRouter()
router.register(r'veterinaria', VeterinariaViewSet, basename='veterinaria')

urlpatterns = [
    path('', include(router.urls)),
]