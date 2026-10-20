from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from django.db import transaction
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from agenda.models import Servicio, Turno
from clinica.models import Veterinaria
from historia_clinica.models import ConsultaClinica, RecetaItem, Vacuna
from internaciones.models import EvolucionInternacion, Internacion
from mascotas.models import Especie, Mascota, Raza
from notificaciones.models import Notificacion
from usuarios.models import HorarioVeterinario, PerfilUsuario, VeterinarioPerfil


@transaction.atomic
def vaciar_datos(nombre_administrador):
    administrador = User.objects.select_for_update().get(username=nombre_administrador)
    if not administrador.is_active or not administrador.is_staff:
        raise ValueError("La cuenta que se conserva debe ser un administrador activo.")

    grupos_admin = list(administrador.groups.values_list("pk", flat=True))
    for modelo in (
        RecetaItem, ConsultaClinica, Vacuna, EvolucionInternacion,
        Internacion, Turno, Notificacion, Mascota, HorarioVeterinario,
        VeterinarioPerfil, PerfilUsuario, Servicio, Raza, Especie, Veterinaria,
        OutstandingToken, Session, LogEntry,
    ):
        modelo.objects.all().delete()

    User.objects.exclude(pk=administrador.pk).delete()
    Group.objects.exclude(pk__in=grupos_admin).delete()
    return administrador.username
