from django.db import models
from core.models import BaseModel

# MODELO SERVICIO
class Servicio(BaseModel):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duracion_estimada = models.PositiveIntegerField(help_text="Duracion en Minutos")

    class Meta:
        db_table = "servicios"
        ordering = ["nombre"]
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.nombre}"


# MODELO TURNO
class Turno(BaseModel):
    class Estado(models.TextChoices):
        RESERVADO = "reservado", "Reservado"
        CONFIRMADO = "confirmado", "Confirmado"
        EN_ESPERA = "en_espera", "En espera"
        EN_CONSULTA = "en_consulta", "En consulta"
        ATENDIDO = "atendido", "Atendido"
        CANCELADO = "cancelado", "Cancelado"

    fecha_hora = models.DateTimeField()

    mascota = models.ForeignKey(
        "mascotas.Mascota",
        on_delete=models.CASCADE,
        related_name="turnos",
    )
    veterinario = models.ForeignKey(
        "usuarios.VeterinarioPerfil",
        on_delete=models.PROTECT,
        related_name="turnos_asignados",
    )
    servicio = models.ForeignKey(
        "agenda.Servicio",
        on_delete=models.PROTECT,
        related_name="turnos",
    )

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.RESERVADO,
    )
    motivo_consulta = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    creado_por_cliente = models.BooleanField(default=False)
    urgencia = models.BooleanField(default=False)

    class Meta:
        db_table = "turnos"
        ordering = ["fecha_hora"]
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha_hora}"

# Este modelo representa los servicios que ofrece la veterinaria (consulta, vacunación, cirugía, etc)
# y los turnos agendados para las mascotas con los veterinarios.
