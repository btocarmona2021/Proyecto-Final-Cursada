from django.db import models
from django.utils import timezone
from core.models import BaseModel

# MODELO INTERNACION
class Internacion(BaseModel):
    class Estado(models.TextChoices):
        INTERNADO = "internado", "Internado"
        OBSERVACION = "observacion", "En observación"
        ALTA = "alta", "Alta médica"
    
    # RELACION CON MASCOTA
    mascota = models.ForeignKey(
        "mascotas.Mascota",
        on_delete=models.CASCADE,
        related_name="internaciones",
    )
    # RELACION CON VETERINARIO
    veterinario_responsable = models.ForeignKey(
        "usuarios.VeterinarioPerfil",
        on_delete=models.PROTECT,
        related_name="internaciones_responsable",
    )

    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    motivo = models.CharField(max_length=255)
    diagnostico_ingreso = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.INTERNADO,
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "internaciones"
        ordering = ["-fecha_ingreso"]
        verbose_name = "Internación"
        verbose_name_plural = "Internaciones"

    def __str__(self):
        return f"Internación {self.mascota.nombre} - {self.fecha_ingreso}"

# MODELOS EVOLUVION INTERNACION
class EvolucionInternacion(BaseModel):
    # RELACION CON INTERNACION
    internacion = models.ForeignKey(
        "internaciones.Internacion",
        on_delete=models.CASCADE,
        related_name="evoluciones",
    )

    # RELACION CON VETERINARIO
    veterinario = models.ForeignKey(
        "usuarios.VeterinarioPerfil",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evoluciones_internacion",
    )
    fecha = models.DateTimeField(default=timezone.now)
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    peso = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    descripcion = models.TextField()
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "evoluciones_internacion"
        ordering = ["-fecha"]
        verbose_name = "Evolución de Internación"
        verbose_name_plural = "Evoluciones de Internación"

    def __str__(self):
        return f"Evolución {self.internacion.mascota.nombre} - {self.fecha}"