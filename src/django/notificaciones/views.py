# notificaciones/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Notificacion
from .serializers import NotificacionSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    """
    Gestión de notificaciones.
    Los usuarios solo ven sus propias notificaciones.
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        SEGURIDAD: Cada usuario solo ve sus notificaciones.
        """
        queryset = Notificacion.objects.select_related("usuario").filter(
            usuario=self.request.user
        )

        leida = self.request.query_params.get("leida")
        if leida is not None:
            queryset = queryset.filter(leida=leida.lower() == "true")

        # Corregido: el modelo tiene 'created_at', no 'fecha_creacion'
        return queryset.order_by("-created_at")