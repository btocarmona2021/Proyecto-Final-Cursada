from django.contrib import admin
from .models import ConsultaClinica, RecetaItem, Vacuna


@admin.register(ConsultaClinica)
class ConsultaClinicaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mascota",
        "veterinario",
        "fecha",
        "tipo",
        "proxima_visita",
        "activo",
    )
    search_fields = (
        "mascota__nombre",
        "veterinario__usuario__first_name",
        "veterinario__usuario__last_name",
        "motivo_consulta",
        "diagnostico",
        "tratamiento",
    )
    list_filter = ("tipo", "activo", "fecha")
    list_select_related = ("mascota", "veterinario", "veterinario__usuario", "turno")


@admin.register(RecetaItem)
class RecetaItemAdmin(admin.ModelAdmin):
    list_display = ("id", "consulta", "medicamento", "dosis", "dias", "activo")
    search_fields = (
        "medicamento",
        "dosis",
        "frecuencia",
        "consulta__mascota__nombre",
    )
    list_filter = ("activo",)
    list_select_related = ("consulta", "consulta__mascota")


@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "mascota",
        "veterinario",
        "fecha_aplicacion",
        "fecha_proxima",
        "activo",
    )
    search_fields = (
        "nombre",
        "mascota__nombre",
        "veterinario__usuario__first_name",
        "veterinario__usuario__last_name",
    )
    list_filter = ("activo", "fecha_aplicacion", "fecha_proxima")
    list_select_related = ("mascota", "veterinario", "veterinario__usuario")