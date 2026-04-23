from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
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

# VIEW MAS BASICAS NO NECESITAN LOGICA DE NEGOCIO USO MODELVIEWSET EL CUAL ME CREA UN CRUD EN UN PAR DE LINEAS
class VeterinariaViewSet(viewsets.ModelViewSet):
    queryset = Veterinaria.objects.all()
    serializer_class = VeterinariaSerializer


class EspecieViewSet(viewsets.ModelViewSet):
    queryset = Especie.objects.all()
    serializer_class = EspecieSerializer


class RazaViewSet(viewsets.ModelViewSet):
    serializer_class = RazaSerializer

    def get_queryset(self):
        queryset = Raza.objects.all()
        especie = self.request.query_params.get("especie")
        if especie:
            queryset = queryset.filter(especie__nombre=especie)  # ← doble guión bajo
        return queryset


class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer


class VeterinarioPerfilViewSet(viewsets.ModelViewSet):
    queryset = VeterinarioPerfil.objects.select_related("usuario").all()
    serializer_class = VeterinarioPerfilSerializer


class HorarioVeterinarioViewSet(viewsets.ModelViewSet):
    queryset = HorarioVeterinario.objects.select_related("veterinario").all()
    serializer_class = HorarioVeterinarioSerializer


class RecetaItemViewSet(viewsets.ModelViewSet):
    queryset = RecetaItem.objects.all()
    serializer_class = RecetaItemSerializer


# ── CON LÓGICA EXTRA ─────────────────────────────────────────────────────────


class RegistroUsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistroUsuarioSerializer


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.select_related("usuario").all()
    serializer_class = PerfilUsuarioSerializer


class MascotaViewSet(viewsets.ModelViewSet):
    serializer_class = MascotaSerializer

    def get_queryset(self):
        queryset = Mascota.objects.select_related("raza__especie", "usuario").all()
        usuario_id = self.request.query_params.get("usuario")
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        return queryset


class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer

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

    def get_queryset(self):
        queryset = Notificacion.objects.select_related("usuario").all()
        usuario_id = self.request.query_params.get("usuario")
        leida = self.request.query_params.get("leida")
        if usuario_id:
            queryset = queryset.filter(usuario__id=usuario_id)
        if leida is not None:
            queryset = queryset.filter(leida=leida.lower() == "true")
        return queryset
