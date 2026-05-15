# internaciones/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from .models import Internacion, EvolucionInternacion
from .serializers import InternacionSerializer, EvolucionInternacionSerializer
from core.permissions import IsVeterinarioOrAdmin


class InternacionViewSet(viewsets.ModelViewSet):
    """
    Gestión de internaciones.

    Reglas de acceso:
    - GET (lista/detalle):
        - Veterinarios/Admin: todas las internaciones.
        - Clientes: solo internaciones de SUS mascotas.
    - POST/PUT/PATCH/DELETE:
        - Solo veterinarios y admins.
    """
    serializer_class = InternacionSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Para métodos de escritura exigimos además IsVeterinarioOrAdmin.
        Para lectura alcanza con estar autenticado.
        """
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsVeterinarioOrAdmin()]

    def get_queryset(self):
        """
        - Vet/Admin: todas las internaciones.
        - Cliente: solo internaciones de mascotas que le pertenecen.
        """
        user = self.request.user

        qs = Internacion.objects.select_related(
            "mascota",
            "mascota__usuario",
            "veterinario_responsable__usuario",
        )

        # Staff médico y admins ven todo
        if user.is_staff or user.groups.filter(name="veterinarios").exists():
            queryset = qs.all()
        else:
            # Cliente: internaciones de SUS mascotas
            queryset = qs.filter(mascota__usuario=user)

        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)

        return queryset


class EvolucionInternacionViewSet(viewsets.ModelViewSet):
    """
    Gestión de evoluciones de internación.
    Solo veterinarios y admins pueden registrar y ver evoluciones por ahora.
    """
    serializer_class = EvolucionInternacionSerializer
    permission_classes = [IsAuthenticated, IsVeterinarioOrAdmin]

    def get_queryset(self):
        queryset = EvolucionInternacion.objects.select_related(
            "internacion",
            "internacion__mascota",
            "veterinario__usuario",
        ).all()

        internacion_id = self.request.query_params.get("internacion")
        if internacion_id:
            queryset = queryset.filter(internacion__id=internacion_id)

        return queryset