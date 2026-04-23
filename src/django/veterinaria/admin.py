from django.contrib import admin
from .models import (
    Veterinaria,
    PerfilUsuario,
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


@admin.register(Veterinaria)
class VeterinariaAdmin(admin.ModelAdmin):
    list_display = ("razon_social", "cuit", "telefono", "email", "activo")
    search_fields = ("razon_social", "cuit")


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id","usuario", "telefono", "direccion")
    search_fields = ("usuario__username", "usuario__email", "usuario__last_name")


@admin.register(VeterinarioPerfil)
class VeterinarioPerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario", "matricula", "especialidad", "disponible")
    search_fields = ("matricula", "usuario__username", "usuario__last_name")
    list_filter = ("disponible",)


@admin.register(HorarioVeterinario)
class HorarioVeterinarioAdmin(admin.ModelAdmin):
    list_display = ("veterinario", "dia_semana", "hora_inicio", "hora_fin", "activo")
    list_filter = ("dia_semana",)


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ("nombre", "emoji", "activo")
    search_fields = ("nombre",)


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ("id","nombre", "especie", "activo")
    list_filter = ("especie",)
    search_fields = ("nombre",)


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "raza", "sexo", "peso_actual", "usuario", "activo")
    search_fields = ("nombre", "microchip")
    list_filter = ("sexo", "raza__especie", "activo")


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_estimada", "activo")
    search_fields = ("nombre",)


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "mascota",
        "veterinario",
        "servicio",
        "fecha_hora",
        "estado",
        "activo",
    )
    list_filter = ("estado", "activo")
    search_fields = ("mascota__nombre", "veterinario__usuario__last_name")


@admin.register(ConsultaClinica)
class ConsultaClinicaAdmin(admin.ModelAdmin):
    list_display = ("mascota", "veterinario", "tipo", "fecha", "activo")
    list_filter = ("tipo", "activo")
    search_fields = ("mascota__nombre",)


@admin.register(RecetaItem)
class RecetaItemAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "consulta", "dosis", "frecuencia", "dias")
    search_fields = ("medicamento", "consulta__mascota__nombre")


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "mascota", "fecha_aplicacion", "fecha_proxima", "activo")
    search_fields = ("nombre", "mascota__nombre")
    list_filter = ("activo",)


@admin.register(Internacion)
class InternacionAdmin(admin.ModelAdmin):
    list_display = (
        "mascota",
        "veterinario_responsable",
        "fecha_ingreso",
        "estado",
        "activo",
    )
    list_filter = ("estado", "activo")
    search_fields = ("mascota__nombre",)


@admin.register(EvolucionInternacion)
class EvolucionInternacionAdmin(admin.ModelAdmin):
    list_display = ("internacion", "veterinario", "fecha", "temperatura", "peso")
    search_fields = ("internacion__mascota__nombre",)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "leida", "activo")
    list_filter = ("tipo", "leida", "activo")
    search_fields = ("titulo", "usuario__username")
