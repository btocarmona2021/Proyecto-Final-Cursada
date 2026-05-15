# usuarios/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import PerfilUsuario, VeterinarioPerfil, HorarioVeterinario
from .serializers import (
    UsuarioSerializer,
    ClienteRegistroSerializer,
    VeterinarioRegistroSerializer,
    PerfilUsuarioSerializer,
    VeterinarioPerfilSerializer,
    HorarioVeterinarioSerializer,
)
from core.permissions import IsAdminUser, IsVeterinarioOrAdmin


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo lectura - para listar usuarios.
    Requiere autenticación.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Registro y gestión de clientes.
    - POST (create): Público (registro abierto)
    - GET/PUT/PATCH/DELETE: Requiere autenticación
    """
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ClienteRegistroSerializer
        return PerfilUsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = ClienteRegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        perfil = PerfilUsuario.objects.get(usuario=user)
        output_serializer = PerfilUsuarioSerializer(perfil)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class VeterinarioViewSet(viewsets.ModelViewSet):
    """
    Registro y gestión de veterinarios.
    - POST (create): Solo administradores
    - GET/PUT/PATCH/DELETE: Requiere autenticación
    """
    queryset = VeterinarioPerfil.objects.all()
    serializer_class = VeterinarioPerfilSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return VeterinarioRegistroSerializer
        return VeterinarioPerfilSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = VeterinarioRegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        perfil = VeterinarioPerfil.objects.get(usuario=user)
        output_serializer = VeterinarioPerfilSerializer(perfil)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class HorarioVeterinarioViewSet(viewsets.ModelViewSet):
    """
    Gestión de horarios de veterinarios.
    Solo veterinarios y admins pueden modificar.
    """
    queryset = HorarioVeterinario.objects.all()
    serializer_class = HorarioVeterinarioSerializer
    permission_classes = [IsAuthenticated, IsVeterinarioOrAdmin]
