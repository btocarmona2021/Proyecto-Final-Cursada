from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel

# MODELO NOTIFICAIONES
class Notificacion(BaseModel):
    class Tipo(models.TextChoices):
        TURNO = "turno", "Turno"
        VACUNA = "vacuna", "Vacuna"
        INTERNACION = "internacion", "Internación"
        SISTEMA = "sistema", "Sistema"

    # RELACION CON USUARIOS
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notificaciones",
    )
    tipo = models.CharField(
        max_length=20,
        choices=Tipo.choices,
    )
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "notificaciones"
        ordering = ["-created_at"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return self.titulo