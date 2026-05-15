from django.contrib import admin
from .models import Internacion, EvolucionInternacion


@admin.register(Internacion)
class InternacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mascota",
        "veterinario_responsable",
        "fecha_ingreso",
        "fecha_egreso",
        "estado",
        "activo",
    )
    search_fields = (
        "mascota__nombre",
        "veterinario_responsable__usuario__first_name",
        "veterinario_responsable__usuario__last_name",
        "motivo",
        "diagnostico_ingreso",
    )
    list_filter = ("estado", "activo", "fecha_ingreso")
    list_select_related = (
        "mascota",
        "veterinario_responsable",
        "veterinario_responsable__usuario",
    )


@admin.register(EvolucionInternacion)
class EvolucionInternacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "internacion",
        "veterinario",
        "fecha",
        "temperatura",
        "peso",
        "activo",
    )
    search_fields = (
        "internacion__mascota__nombre",
        "veterinario__usuario__first_name",
        "veterinario__usuario__last_name",
        "descripcion",
        "indicaciones",
    )
    list_filter = ("activo", "fecha")
    list_select_related = ("internacion", "internacion__mascota", "veterinario", "veterinario__usuario")