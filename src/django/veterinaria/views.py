from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .tokens import TokenPersonalizado
from .models import (
    Especie,
    Raza,
    Servicio,
    Veterinaria,
    PerfilUsuario,
    VeterinarioPerfil,
    HorarioVeterinario,
    Mascota,
    Turno,
    ConsultaClinica,
    RecetaItem,
    Vacuna,
    Internacion,
    EvolucionInternacion,
    Notificacion,
)
from .serializers import (
    EspecieSerializer,
    RazaSerializer,
    ServicioSerializer,
    VeterinariaSerializer,
    PerfilUsuarioSerializer,
    RegistroUsuarioSerializer,
    VeterinarioPerfilSerializer,
    HorarioVeterinarioSerializer,
    MascotaSerializer,
    TurnoSerializer,
    ConsultaClinicaSerializer,
    RecetaItemSerializer,
    VacunaSerializer,
    InternacionSerializer,
    EvolucionInternacionSerializer,
    NotificacionSerializer,
)


class VeterinariaViewSet(viewsets.ModelViewSet):
    queryset = Veterinaria.objects.all()
    serializer_class = VeterinariaSerializer
    permission_classes = [IsAuthenticated]


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer
    permission_classes = [IsAuthenticated]


class RazaViewSet(viewsets.ModelViewSet):
    serializer_class = RazaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Raza.objects.all()
        especie = self.request.query_params.get("especie")
        if especie:
            queryset = queryset.filter(especie__nombre=especie)
        return queryset


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
    permission_classes = [IsAuthenticated]


class VeterinarioPerfilViewSet(viewsets.ModelViewSet):
    queryset = VeterinarioPerfil.objects.select_related("usuario").all()
    serializer_class = VeterinarioPerfilSerializer
    permission_classes = [IsAuthenticated]


class HorarioVeterinarioViewSet(viewsets.ModelViewSet):
    queryset = HorarioVeterinario.objects.select_related("veterinario").all()
    serializer_class = HorarioVeterinarioSerializer
    permission_classes = [IsAuthenticated]


class RecetaItemViewSet(viewsets.ModelViewSet):
    queryset = RecetaItem.objects.all()
    serializer_class = RecetaItemSerializer
    permission_classes = [IsAuthenticated]


class RegistroUsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsAuthenticated]


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.select_related("usuario").all()
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]


class MascotaViewSet(viewsets.ModelViewSet):
    serializer_class = MascotaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Mascota.objects.select_related("raza__especie", "usuario").all()
        usuario_id = self.request.query_params.get("usuario")
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        return queryset


class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Turno.objects.select_related(
            "mascota", "veterinario__usuario", "servicio"
        ).all()
        estado = self.request.query_params.get("estado")
        mascota_id = self.request.query_params.get("mascota")
        if estado:
            queryset = queryset.filter(estado=estado)
        if mascota_id:
            queryset = queryset.filter(mascota__id=mascota_id)
        return queryset


class ConsultaClinicaViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultaClinicaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            ConsultaClinica.objects.select_related("mascota", "veterinario__usuario")
            .prefetch_related("recetas")
            .all()
        )
        mascota_id = self.request.query_params.get("mascota")
        if mascota_id:
            queryset = queryset.filter(mascota__id=mascota_id)
        return queryset


class VacunaViewSet(viewsets.ModelViewSet):
    serializer_class = VacunaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Vacuna.objects.select_related(
            "mascota", "veterinario__usuario"
        ).all()
        mascota_id = self.request.query_params.get("mascota")
        if mascota_id:
            queryset = queryset.filter(mascota__id=mascota_id)
        return queryset


class InternacionViewSet(viewsets.ModelViewSet):
    serializer_class = InternacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Internacion.objects.select_related(
            "mascota", "veterinario_responsable__usuario"
        ).all()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset


class EvolucionInternacionViewSet(viewsets.ModelViewSet):
    serializer_class = EvolucionInternacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = EvolucionInternacion.objects.select_related(
            "internacion", "veterinario__usuario"
        ).all()
        internacion_id = self.request.query_params.get("internacion")
        if internacion_id:
            queryset = queryset.filter(internacion__id=internacion_id)
        return queryset


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Notificacion.objects.select_related("usuario").all()
        usuario_id = self.request.query_params.get("usuario")
        leida = self.request.query_params.get("leida")
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        if leida is not None:
            queryset = queryset.filter(leida=leida.lower() == "true")
        return queryset


# LOGIN PERSONALIZADO CON ROL
class LoginView(TokenObtainPairView):
    serializer_class = TokenPersonalizado
