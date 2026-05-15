# agenda/views.py (turnos)
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Turno, Servicio
from .serializers import (
    TurnoSerializer,
    TurnoCreateSerializer,
    ServicioSerializer
)
from core.permissions import CanManageTurno, CanManageServicio


class ServicioViewSet(viewsets.ModelViewSet):
    """
    Gestión de servicios.
    - GET: Todos pueden ver
    - POST/PUT/PATCH/DELETE: Solo admins
    """
    queryset = Servicio.objects.filter(activo=True)
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated, CanManageServicio]


class TurnoViewSet(viewsets.ModelViewSet):
    """
    Gestión de turnos.
    - GET: Todos (filtrado por get_queryset)
    - POST: Todos (validado en perform_create)
    - PUT/PATCH/DELETE: Solo veterinarios/admins

    SEGURIDAD: 
    - Clientes solo ven turnos de SUS mascotas
    - Clientes solo crean turnos para SUS mascotas
    """
    permission_classes = [IsAuthenticated, CanManageTurno]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TurnoCreateSerializer
        return TurnoSerializer

    def get_queryset(self):
        """
        SEGURIDAD (GET):
        - Clientes: solo ven turnos de SUS mascotas
        - Veterinarios/Admins: ven TODOS los turnos
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
        SEGURIDAD (POST):
        - Clientes: pueden crear turnos SOLO para SUS mascotas
        - Veterinarios/Admins: pueden crear turnos para CUALQUIER mascota
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