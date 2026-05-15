from django.db import models
from django.utils import timezone
from core.models import BaseModel

# MODELOS CONSULTA CLINICA
class ConsultaClinica(BaseModel):
    class TipoConsulta(models.TextChoices):
        CONTROL = "control", "Control general"
        VACUNACION = "vacunacion", "Vacunación"
        CIRUGIA = "cirugia", "Cirugía"
        URGENCIA = "urgencia", "Urgencia"
        POST_OPERATORIO = "post_operatorio", "Post-operatorio"
        DESPARASITACION = "desparasitacion", "Desparasitación"
        OTRO = "otro", "Otro"

    # RELACION CON MASCOTA
    mascota = models.ForeignKey(
        "mascotas.Mascota", on_delete=models.CASCADE, related_name="consultas"
    )
    # RELACION CON TURNO
    turno = models.OneToOneField(
        "agenda.Turno",
        on_delete=models.SET_NULL,
        related_name="consulta_clinica",
        null=True,
    )

    fecha = models.DateTimeField(default=timezone.now)

    # RELACION CON VETERINARIO
    veterinario = models.ForeignKey(
        "usuarios.VeterinarioPerfil",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consultas_clinicas",
    )

    tipo = models.CharField(
        max_length=30, choices=TipoConsulta.choices, default=TipoConsulta.CONTROL
    )

    motivo_consulta = models.CharField(max_length=255, blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    peso_actual = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    frecuencia_cardiaca = models.PositiveIntegerField(null=True, blank=True)
    frecuencia_respiratoria = models.PositiveIntegerField(null=True, blank=True)
    proxima_visita = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "consultas_clinicas"
        ordering = ["-fecha"]
        verbose_name = "Consulta Clinica"
        verbose_name_plural = "Consultas Clinicas"

    def __str__(self):
        return f"Consulta {self.id} - {self.mascota.nombre}"


# MODELO RECETA
class RecetaItem(BaseModel):
    # RELACION CON CONSULTA CLINICA
    consulta = models.ForeignKey(
        ConsultaClinica, on_delete=models.CASCADE, related_name="recetas"
    )
    medicamento = models.CharField(max_length=150)
    dosis = models.CharField(max_length=150)
    frecuencia = models.CharField(max_length=150, blank=True, null=True)
    dias = models.PositiveIntegerField(blank=True, null=True)
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "receta_items"
        ordering = ["consulta", "id"]
        verbose_name = "Item de Receta"
        verbose_name_plural = "Items de Receta"

    def __str__(self):
        return f"{self.medicamento} - {self.consulta.mascota.nombre}"


# MODELO VACUNA
class Vacuna(BaseModel):
    mascota = models.ForeignKey(
        "mascotas.Mascota", on_delete=models.CASCADE, related_name="vacunas"
    )
    nombre = models.CharField(max_length=120)
    fecha_aplicacion = models.DateField()
    fecha_proxima = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    veterinario = models.ForeignKey(
        "usuarios.VeterinarioPerfil",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vacunas_aplicadas",
    )

    class Meta:
        db_table = "vacunas"
        ordering = ["-fecha_aplicacion"]
        verbose_name = "Vacuna"
        verbose_name_plural = "Vacunas"

    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"

