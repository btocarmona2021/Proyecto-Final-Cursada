from django.contrib import admin
from .models import Servicio, Turno


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "duracion_estimada", "activo")
    search_fields = ("nombre", "descripcion")
    list_filter = ("activo",)


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fecha_hora",
        "mascota",
        "veterinario",
        "servicio",
        "estado",
        "creado_por_cliente",
        "activo",
    )
    search_fields = (
        "mascota__nombre",
        "veterinario__usuario__first_name",
        "veterinario__usuario__last_name",
        "veterinario__matricula",
        "servicio__nombre",
        "motivo_consulta",
    )
    list_filter = ("estado", "creado_por_cliente", "activo", "servicio")
    list_select_related = (
        "mascota",
        "veterinario",
        "veterinario__usuario",
        "servicio",
    )
