# historia_clinica/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ConsultaClinica, RecetaItem, Vacuna
from .serializers import (
    ConsultaClinicaSerializer,
    RecetaItemSerializer,
    VacunaSerializer,
)
from core.permissions import IsVeterinarioOrAdmin


class ConsultaClinicaViewSet(viewsets.ModelViewSet):
    """
    Gestión de consultas clínicas.
    Solo veterinarios y admins pueden crear/modificar consultas.
    Clientes pueden VER las consultas de SUS mascotas (filtrado en get_queryset).
    """
    serializer_class = ConsultaClinicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        SEGURIDAD:
        - Veterinarios/Admins: ven TODAS las consultas
        - Clientes: solo consultas de SUS mascotas
        """
        user = self.request.user
        queryset = (
            ConsultaClinica.objects.select_related("mascota", "veterinario__usuario")
            .prefetch_related("recetas")
            .all()
        )

        # Si es cliente, filtrar por sus mascotas
        if user.groups.filter(name="clientes").exists():
            queryset = queryset.filter(mascota__usuario=user)

        mascota_id = self.request.query_params.get("mascota")
        if mascota_id:
            queryset = queryset.filter(mascota__id=mascota_id)

        return queryset.order_by('-fecha')

    def get_permissions(self):
        """
        - GET: Todos (filtrado en get_queryset)
        - POST/PUT/PATCH/DELETE: Solo veterinarios/admins
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVeterinarioOrAdmin()]


class RecetaItemViewSet(viewsets.ModelViewSet):
    """
    Gestión de ítems de recetas.
    Solo veterinarios y admins pueden gestionar recetas.
    """
    queryset = RecetaItem.objects.select_related("consulta").all()
    serializer_class = RecetaItemSerializer
    permission_classes = [IsAuthenticated, IsVeterinarioOrAdmin]


class VacunaViewSet(viewsets.ModelViewSet):
    """
    Gestión de vacunas.
    Solo veterinarios y admins pueden registrar vacunas.
    Clientes pueden VER las vacunas de SUS mascotas.
    """
    serializer_class = VacunaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        SEGURIDAD:
        - Veterinarios/Admins: ven TODAS las vacunas
        - Clientes: solo vacunas de SUS mascotas
        """
        user = self.request.user
        queryset = Vacuna.objects.select_related(
            "mascota", "veterinario__usuario"
        ).all()

        # Si es cliente, filtrar por sus mascotas
        if user.groups.filter(name="clientes").exists():
            queryset = queryset.filter(mascota__usuario=user)

        mascota_id = self.request.query_params.get("mascota")
        if mascota_id:
            queryset = queryset.filter(mascota__id=mascota_id)

        return queryset.order_by('-fecha_aplicacion')

    def get_permissions(self):
        """
        - GET: Todos (filtrado en get_queryset)
        - POST/PUT/PATCH/DELETE: Solo veterinarios/admins
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVeterinarioOrAdmin()]
