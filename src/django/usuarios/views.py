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
from core.permissions import IsAdminUser, IsVeterinarioOrAdmin ,CanManageVeterinarioPerfil,CanManageClientePerfil


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Solo los administradores autenticados pueden listar,
    consultar y eliminar usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        usuario = self.get_object()
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClienteViewSet(viewsets.ModelViewSet):
    """
    Registro y gestión de clientes.
    - Registro: público.
    - Las demás operaciones requieren autenticación.
    - Administradores: consultan, editan y eliminan cualquier perfil.
    - Veterinarios: consultan todos los perfiles.
    - Clientes: consultan y editan únicamente su propio perfil.
    """
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer


    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.groups.filter(name='veterinarios').exists():
            # Veterinario/Admin puede ver todos los clientes
            return PerfilUsuario.objects.all()

        return PerfilUsuario.objects.filter(usuario=user)  # Cliente solo su propio perfil

    def get_serializer_class(self):
        if self.action == 'create':
            return ClienteRegistroSerializer
        return PerfilUsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated(), CanManageClientePerfil()]

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
    - Consulta: usuarios autenticados.
    - Creación, edición y eliminación: solo administradores.
    """
    queryset = VeterinarioPerfil.objects.all()
    serializer_class = VeterinarioPerfilSerializer
    permission_classes = [IsAuthenticated, CanManageVeterinarioPerfil]  

    def get_serializer_class(self):
        if self.action == 'create':
            return VeterinarioRegistroSerializer
        return VeterinarioPerfilSerializer

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
