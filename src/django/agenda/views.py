# agenda/views.py (turnos)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .models import Turno, Servicio
from .serializers import (
    TurnoSerializer,
    TurnoCreateSerializer,
    ServicioSerializer
)
from core.permissions import CanManageTurno, CanManageServicio, CanCancelTurno, IsVeterinarioOrAdmin


class ServicioViewSet(viewsets.ModelViewSet):
    """
    Gestión de servicios.
    - GET: Todos pueden ver
    - POST/PUT/PATCH/DELETE: Solo admins
    """
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated, CanManageServicio]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), CanManageServicio()]


class TurnoViewSet(viewsets.ModelViewSet):
    """
    Gestión de turnos.
    - GET: Todos (filtrado por get_queryset)
    - POST: Todos (validado en perform_create)
    - PUT/PATCH/DELETE: Solo veterinarios/admins

    Los clientes solo ven y crean turnos de sus propias mascotas.
    """
    permission_classes = [IsAuthenticated, CanManageTurno]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TurnoCreateSerializer
        return TurnoSerializer

    def get_queryset(self):
        """
        Los clientes solo ven los turnos de sus mascotas.
        Veterinarios y admins ven todos los turnos.
        """
        queryset = Turno.objects.select_related(
            "mascota",
            "mascota__usuario",
            "veterinario__usuario",
            "servicio"
        )

        user = self.request.user

        if user.groups.filter(name="clientes").exists():
            queryset = queryset.filter(mascota__usuario=user)

        # Filtros opcionales
        estado = self.request.query_params.get("estado")
        mascota_id = self.request.query_params.get("mascota_id")
        veterinario_id = self.request.query_params.get("veterinario_id")
        usuario_id = self.request.query_params.get("usuario_id")

        if estado:
            queryset = queryset.filter(estado=estado)
        if mascota_id:
            queryset = queryset.filter(mascota_id=mascota_id)
        if veterinario_id:
            queryset = queryset.filter(veterinario_id=veterinario_id)
        if usuario_id:
            queryset = queryset.filter(mascota__usuario_id=usuario_id)

        return queryset

    def perform_create(self, serializer):
        """
        Los clientes solo pueden crear turnos para sus mascotas.
        Veterinarios y admins pueden crear turnos para cualquier mascota.
        """
        user = self.request.user
        mascota = serializer.validated_data.get('mascota')

        if user.groups.filter(name="clientes").exists():
            if mascota.usuario != user:
                raise PermissionDenied(
                    "No puede crear turnos para mascotas que no son suyas."
                )
            serializer.save(creado_por_cliente=True)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = TurnoCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        turno = serializer.instance
        output_serializer = TurnoSerializer(turno)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = TurnoCreateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.refresh_from_db()
        output_serializer = TurnoSerializer(instance)
        return Response(output_serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, CanCancelTurno])
    def cancelar(self, request, pk=None):
        """Cancela un turno. El cliente solo puede cancelar sus propios turnos."""
        turno = self.get_object()
        turno.estado = Turno.Estado.CANCELADO
        turno.save()
        serializer = TurnoSerializer(turno)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsVeterinarioOrAdmin])
    def atender(self, request, pk=None):
        """Marca el turno como atendido. Solo veterinarios y admins."""
        turno = self.get_object()
        turno.estado = Turno.Estado.ATENDIDO
        turno.save()
        serializer = TurnoSerializer(turno)
        return Response(serializer.data)