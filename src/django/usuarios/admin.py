from django.contrib import admin
from .models import PerfilUsuario, VeterinarioPerfil, HorarioVeterinario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "telefono", "direccion", "fecha_creacion")
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "telefono",
        "direccion",
    )
    list_select_related = ("usuario",)


@admin.register(VeterinarioPerfil)
class VeterinarioPerfilAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "matricula",
        "especialidad",
        "disponible",
        "fecha_creacion",
    )
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "matricula",
        "especialidad",
    )
    list_filter = ("disponible",)
    list_select_related = ("usuario",)


@admin.register(HorarioVeterinario)
class HorarioVeterinarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "veterinario",
        "dia_semana",
        "hora_inicio",
        "hora_fin",
        "activo",
    )
    list_filter = ("dia_semana", "activo")
    search_fields = (
        "veterinario__usuario__first_name",
        "veterinario__usuario__last_name",
        "veterinario__matricula",
    )
    list_select_related = ("veterinario", "veterinario__usuario")