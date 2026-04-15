from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("activo", True)

        # Crear o buscar el rol "admin" automáticamente
        rol_admin, _ = Rol.objects.get_or_create(
            nombre="admin",
            defaults={"descripcion": "Administrador del sistema"}
        )
        extra_fields.setdefault("rol", rol_admin)

        # Campos obligatorios del modelo
        extra_fields.setdefault("nombre", "Admin")
        extra_fields.setdefault("apellido", "Sistema")

        return self.create_user(email, password, **extra_fields)


class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Rol(BaseModel):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "roles"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Usuario(AbstractBaseUser, PermissionsMixin, BaseModel):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, related_name="usuarios")
    disponible = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        db_table = "usuarios"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"


class VeterinarioPerfil(BaseModel):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="perfil_veterinario"
    )
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.CharField(max_length=120, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "veterinarios_perfiles"
        ordering = ["usuario__apellido", "usuario__nombre"]

    def __str__(self):
        return self.usuario.nombre_completo


class HorarioVeterinario(BaseModel):
    class DiaSemana(models.IntegerChoices):
        LUNES = 1, "Lunes"
        MARTES = 2, "Martes"
        MIERCOLES = 3, "Miércoles"
        JUEVES = 4, "Jueves"
        VIERNES = 5, "Viernes"
        SABADO = 6, "Sábado"
        DOMINGO = 7, "Domingo"

    veterinario = models.ForeignKey(
        VeterinarioPerfil, on_delete=models.CASCADE, related_name="horarios"
    )
    dia_semana = models.PositiveSmallIntegerField(choices=DiaSemana.choices)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    class Meta:
        db_table = "horarios_veterinarios"
        ordering = ["veterinario", "dia_semana", "hora_inicio"]

    def __str__(self):
        return f"{self.veterinario} - {self.get_dia_semana_display()} {self.hora_inicio}-{self.hora_fin}"


class Especie(BaseModel):
    nombre = models.CharField(max_length=80, unique=True)
    emoji = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = "especies"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Raza(BaseModel):
    class Tamano(models.TextChoices):
        PEQUENO = "pequeno", "Pequeño"
        MEDIANO = "mediano", "Mediano"
        GRANDE = "grande", "Grande"
        VARIABLE = "variable", "Variable"

    especie = models.ForeignKey(Especie, on_delete=models.PROTECT, related_name="razas")
    nombre = models.CharField(max_length=120)
    tamano = models.CharField(
        max_length=20, choices=Tamano.choices, default=Tamano.VARIABLE
    )

    class Meta:
        db_table = "razas"
        ordering = ["nombre"]
        unique_together = ("especie", "nombre")

    def __str__(self):
        return f"{self.nombre} ({self.especie.nombre})"


class Mascota(BaseModel):
    class Sexo(models.TextChoices):
        MACHO = "M", "Macho"
        HEMBRA = "H", "Hembra"

    nombre = models.CharField(max_length=120)
    raza = models.ForeignKey(Raza, on_delete=models.PROTECT, related_name="mascotas")
    fecha_nacimiento = models.DateField(blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, blank=True, null=True)
    color = models.CharField(max_length=80, blank=True, null=True)
    peso_actual = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    microchip = models.CharField(max_length=50, blank=True, null=True, unique=True)
    observaciones_generales = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="mascotas"
    )
    fecha_registro = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "mascotas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Servicio(BaseModel):
    nombre = models.CharField(max_length=120)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    duracion_estimada = models.PositiveIntegerField(help_text="Duración en minutos")

    class Meta:
        db_table = "servicios"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


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
        Mascota, on_delete=models.CASCADE, related_name="turnos"
    )
    veterinario = models.ForeignKey(
        VeterinarioPerfil, on_delete=models.PROTECT, related_name="turnos_asignados"
    )
    servicio = models.ForeignKey(
        Servicio, on_delete=models.PROTECT, related_name="turnos"
    )
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.RESERVADO
    )
    motivo_consulta = models.CharField(max_length=255, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    creado_por_cliente = models.BooleanField(default=False)

    class Meta:
        db_table = "turnos"
        ordering = ["fecha_hora"]

    def __str__(self):
        return f"{self.mascota.nombre} - {self.fecha_hora}"


class ConsultaClinica(BaseModel):
    class TipoConsulta(models.TextChoices):
        CONTROL = "control", "Control general"
        VACUNACION = "vacunacion", "Vacunación"
        CIRUGIA = "cirugia", "Cirugía"
        URGENCIA = "urgencia", "Urgencia"
        POST_OPERATORIO = "post_operatorio", "Post-operatorio"
        DESPARASITACION = "desparasitacion", "Desparasitación"
        OTRO = "otro", "Otro"

    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="consultas"
    )
    turno = models.OneToOneField(
        Turno,
        on_delete=models.SET_NULL,
        related_name="consulta_clinica",
        null=True,
        blank=True,
    )
    fecha = models.DateTimeField(default=timezone.now)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
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

    def __str__(self):
        return f"Consulta {self.id} - {self.mascota.nombre}"


class RecetaItem(BaseModel):
    consulta = models.ForeignKey(
        ConsultaClinica, on_delete=models.CASCADE, related_name="recetas"
    )
    medicamento = models.CharField(max_length=150)
    dosis = models.CharField(max_length=150)
    frecuencia = models.CharField(max_length=150, blank=True, null=True)
    dias = models.PositiveIntegerField(blank=True, null=True)
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "recetas_items"
        ordering = ["consulta", "id"]

    def __str__(self):
        return f"{self.medicamento} - {self.consulta.mascota.nombre}"


class Vacuna(BaseModel):
    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="vacunas"
    )
    nombre = models.CharField(max_length=120)
    fecha_aplicacion = models.DateField()
    fecha_proxima = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vacunas_aplicadas",
    )

    class Meta:
        db_table = "vacunas"
        ordering = ["-fecha_aplicacion"]

    def __str__(self):
        return f"{self.nombre} - {self.mascota.nombre}"


class Internacion(BaseModel):
    class Estado(models.TextChoices):
        INTERNADO = "internado", "Internado"
        OBSERVACION = "observacion", "En observación"
        ALTA = "alta", "Alta médica"

    mascota = models.ForeignKey(
        Mascota, on_delete=models.CASCADE, related_name="internaciones"
    )
    veterinario_responsable = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.PROTECT,
        related_name="internaciones_responsable",
    )
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_egreso = models.DateTimeField(blank=True, null=True)
    motivo = models.CharField(max_length=255)
    diagnostico_ingreso = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.INTERNADO
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "internaciones"
        ordering = ["-fecha_ingreso"]

    def __str__(self):
        return f"Internación {self.mascota.nombre} - {self.fecha_ingreso}"


class EvolucionInternacion(BaseModel):
    internacion = models.ForeignKey(
        Internacion, on_delete=models.CASCADE, related_name="evoluciones"
    )
    fecha = models.DateTimeField(default=timezone.now)
    veterinario = models.ForeignKey(
        VeterinarioPerfil,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evoluciones_internacion",
    )
    temperatura = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    peso = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    descripcion = models.TextField()
    indicaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "evoluciones_internacion"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Evolución {self.internacion.mascota.nombre} - {self.fecha}"


class Notificacion(BaseModel):
    class Tipo(models.TextChoices):
        TURNO = "turno", "Turno"
        VACUNA = "vacuna", "Vacuna"
        INTERNACION = "internacion", "Internación"
        SISTEMA = "sistema", "Sistema"

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="notificaciones"
    )
    tipo = models.CharField(max_length=20, choices=Tipo.choices)
    titulo = models.CharField(max_length=150)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_lectura = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "notificaciones"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return self.titulo
