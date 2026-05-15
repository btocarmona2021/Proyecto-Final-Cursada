# mascotas/views.py
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Mascota, Especie, Raza
from .serializers import (
    MascotaSerializer,
    MascotaCreateSerializer,
    EspecieSerializer,
    RazaSerializer
)
from core.permissions import CanManageMascota, CanManageEspecieRaza


class EspecieViewSet(viewsets.ModelViewSet):
    """
    Gestión de especies.
    - GET: Todos pueden ver
    - POST/PUT/PATCH/DELETE: Solo admins
    """
    queryset = Especie.objects.filter(activo=True)
    serializer_class = EspecieSerializer
    permission_classes = [IsAuthenticated, CanManageEspecieRaza]


class RazaViewSet(viewsets.ModelViewSet):
    """
    Gestión de razas.
    - GET: Todos pueden ver (con filtro por especie)
    - POST/PUT/PATCH/DELETE: Solo admins
    """
    queryset = Raza.objects.filter(activo=True)
    serializer_class = RazaSerializer
    permission_classes = [IsAuthenticated, CanManageEspecieRaza]

    def get_queryset(self):
        queryset = super().get_queryset()
        especie_id = self.request.query_params.get('especie_id')
        if especie_id:
            queryset = queryset.filter(especie_id=especie_id)
        return queryset


class MascotaViewSet(viewsets.ModelViewSet):
    """
    Gestión de mascotas.
    - GET: Todos (filtrado automático por get_queryset)
    - POST: Solo veterinarios/admins
    - PUT/PATCH/DELETE: Dueño o staff

    SEGURIDAD: Clientes solo ven SUS mascotas.
    """
    queryset = Mascota.objects.select_related('raza', 'raza__especie', 'usuario')
    permission_classes = [IsAuthenticated, CanManageMascota]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MascotaCreateSerializer
        return MascotaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # SEGURIDAD: Si es cliente, solo ve SUS mascotas
        if user.groups.filter(name="clientes").exists():
            queryset = queryset.filter(usuario=user)

        # Filtros opcionales
        usuario_id = self.request.query_params.get('usuario_id')
        if usuario_id:
            queryset = queryset.filter(usuario_id=usuario_id)

        # Solo activas por defecto
        solo_activas = self.request.query_params.get('solo_activas', 'true')
        if solo_activas.lower() == 'true':
            queryset = queryset.filter(activo=True)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = MascotaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mascota = serializer.save()
        output_serializer = MascotaSerializer(mascota)
        return Response(output_serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = MascotaCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        mascota = serializer.save()
        output_serializer = MascotaSerializer(mascota)
        return Response(output_serializer.data)
