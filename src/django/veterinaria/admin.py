from django.contrib import admin
from .models import (
    Rol,
    Usuario,
    VeterinarioPerfil,
    HorarioVeterinario,
    Especie,
    Raza,
    Mascota,
    Servicio,
    Turno,
    ConsultaClinica,
    RecetaItem,
    Vacuna,
    Internacion,
    EvolucionInternacion,
    Notificacion,
)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "activo")
    search_fields = ("nombre",)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "nombre", "apellido", "rol", "is_staff", "activo")
    search_fields = ("email", "nombre", "apellido")
    list_filter = ("rol", "is_staff", "activo")


@admin.register(VeterinarioPerfil)
class VeterinarioPerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "matricula", "especialidad")
    search_fields = ("matricula", "usuario__email")


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emoji", "activo")


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "especie", "tamano", "activo")
    list_filter = ("especie", "tamano")


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "raza", "sexo", "peso_actual", "usuario", "activo")
    search_fields = ("nombre", "microchip")
    list_filter = ("sexo", "raza__especie")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_estimada", "activo")


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario", "servicio", "fecha_hora", "estado")
    list_filter = ("estado",)
    search_fields = ("mascota__nombre",)


@admin.register(ConsultaClinica)
class ConsultaClinicaAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario", "tipo", "fecha")
    list_filter = ("tipo",)


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "mascota", "fecha_aplicacion", "fecha_proxima")


@admin.register(Internacion)
class InternacionAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario_responsable", "fecha_ingreso", "estado")
    list_filter = ("estado",)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "leida")
    list_filter = ("tipo", "leida")
