from django.contrib import admin
from .models import Especie, Raza, Mascota


@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "emoji", "activo")
    search_fields = ("nombre",)
    list_filter = ("activo",)


@admin.register(Raza)
class RazaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "especie", "activo")
    search_fields = ("nombre", "especie__nombre")
    list_filter = ("activo", "especie")
    list_select_related = ("especie",)


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "usuario",
        "raza",
        "sexo",
        "peso_actual",
        "microchip",
        "activo",
    )
    search_fields = (
        "nombre",
        "microchip",
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "raza__nombre",
        "raza__especie__nombre",
    )
    list_filter = ("activo", "sexo", "raza__especie", "raza")
    list_select_related = ("usuario", "raza", "raza__especie")