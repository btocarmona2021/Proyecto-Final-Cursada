from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "tipo",
        "titulo",
        "leida",
        "fecha_lectura",
        "created_at",
        "activo",
    )
    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "usuario__email",
        "titulo",
        "mensaje",
    )
    list_filter = ("tipo", "leida", "activo", "created_at")
    list_select_related = ("usuario",)