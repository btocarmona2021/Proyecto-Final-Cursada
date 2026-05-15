# clinica/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Veterinaria
from .serializers import VeterinariaSerializer
from core.permissions import IsAdminUser


class VeterinariaViewSet(viewsets.ModelViewSet):
    """
    Gestión de datos de la veterinaria.
    - GET: Todos pueden ver
    - POST/PUT/PATCH/DELETE: Solo admins
    """
    queryset = Veterinaria.objects.all()
    serializer_class = VeterinariaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]
