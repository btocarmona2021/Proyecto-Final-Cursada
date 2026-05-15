# usuarios/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.token_personalizado import CustomTokenObtainPairView
from usuarios.views import (
    UsuarioViewSet,
    ClienteViewSet,
    VeterinarioViewSet,
    HorarioVeterinarioViewSet,
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'clientes', ClienteViewSet, basename='cliente')
router.register(r'veterinarios', VeterinarioViewSet, basename='veterinario')
router.register(r'horarios', HorarioVeterinarioViewSet, basename='horario')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]