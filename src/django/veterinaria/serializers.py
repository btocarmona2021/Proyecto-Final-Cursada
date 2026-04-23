from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Veterinaria,
    PerfilUsuario,
    VeterinarioPerfil,
    HorarioVeterinario,
    Especie,
    Raza,
    Mascota,
    Servicio,
    Turno,
    ConsultaClinica,
    RecetaItem,
    Vacuna,
    Internacion,
    EvolucionInternacion,
    Notificacion,
)


class VeterinariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinaria
        fields = [
            "id",
            "razon_social",
            "nombre_fantasia",
            "cuit",
            "direccion",
            "ciudad",
            "provincia",
            "codigo_postal",
            "telefono",
            "email",
            "sitio_web",
            "logo",
            "descripcion",
            "horario_atencion",
            "instagram",
            "facebook",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)

    class Meta:
        model = PerfilUsuario
        fields = ["id", "usuario", "telefono", "direccion", "foto"]


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    direccion = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "telefono",
            "direccion",
        ]

    def create(self, validated_data):
        telefono = validated_data.pop("telefono", None)
        direccion = validated_data.pop("direccion", None)
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        PerfilUsuario.objects.create(
            usuario=user,
            telefono=telefono,
            direccion=direccion,
        )
        return user


class VeterinarioPerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = VeterinarioPerfil
        fields = [
            "id",
            "usuario",
            "nombre_completo",
            "matricula",
            "especialidad",
            "biografia",
            "foto",
            "disponible",
        ]


class HorarioVeterinarioSerializer(serializers.ModelSerializer):
    dia_semana_display = serializers.CharField(
        source="get_dia_semana_display", read_only=True
    )
    nombre_veterinario = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )

    class Meta:
        model = HorarioVeterinario
        fields = [
            "id",
            "veterinario",
            "nombre_veterinario",
            "dia_semana",
            "dia_semana_display",
            "hora_inicio",
            "hora_fin",
        ]

    def validate(self, data):
        veterinario = data.get(
            "veterinario", getattr(self.instance, "veterinario", None)
        )
        dia_semana = data.get("dia_semana", getattr(self.instance, "dia_semana", None))
        hora_inicio = data.get(
            "hora_inicio", getattr(self.instance, "hora_inicio", None)
        )
        hora_fin = data.get("hora_fin", getattr(self.instance, "hora_fin", None))

        solapados = HorarioVeterinario.objects.filter(
            veterinario=veterinario,
            dia_semana=dia_semana,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )

        # Al editar excluye el registro actual
        if self.instance:
            solapados = solapados.exclude(pk=self.instance.pk)

        if solapados.exists():
            raise serializers.ValidationError(
                "El horario se solapa con un horario existente para ese día."
            )

        return data


class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = ["id", "nombre", "emoji"]


class RazaSerializer(serializers.ModelSerializer):
    especie_nombre = serializers.CharField(source="especie.nombre", read_only=True)

    class Meta:
        model = Raza
        fields = ["id", "nombre", "especie", "especie_nombre"]


class MascotaSerializer(serializers.ModelSerializer):
    raza_nombre = serializers.CharField(source="raza.nombre", read_only=True)
    especie_nombre = serializers.CharField(source="raza.especie.nombre",read_only=True)
    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name", read_only=True
    )

    class Meta:
        model = Mascota
        fields = [
            "id",
            "nombre",
            "raza",
            "raza_nombre",
            "especie_nombre",
            "fecha_nacimiento",
            "sexo",
            "color",
            "peso_actual",
            "microchip",
            "foto",
            "usuario",
            "usuario_nombre",
        ]


class ServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ["id", "nombre", "descripcion", "precio", "duracion_estimada"]


class TurnoSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    
    veterinario_nombre = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )
    servicio_nombre = serializers.CharField(source="servicio.nombre", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Turno
        fields = [
            "id",
            "fecha_hora",
            "mascota",
            "mascota_nombre",
            "veterinario",
            "veterinario_nombre",
            "servicio",
            "servicio_nombre",
            "estado",
            "estado_display",
            "motivo_consulta",
            "notas",
            "creado_por_cliente",
        ]

    def validate(self, data):
        from datetime import timedelta

        veterinario = data.get(
            "veterinario", getattr(self.instance, "veterinario", None)
        )
        fecha_hora = data.get("fecha_hora", getattr(self.instance, "fecha_hora", None))
        servicio = data.get("servicio", getattr(self.instance, "servicio", None))

        # 1. Validar que el turno esté dentro del horario del veterinario
        dia_semana = fecha_hora.isoweekday()  # 1=Lunes ... 7=Domingo
        hora = fecha_hora.time()

        horario_valido = HorarioVeterinario.objects.filter(
            veterinario=veterinario,
            dia_semana=dia_semana,
            hora_inicio__lte=hora,
            hora_fin__gte=hora,
        ).exists()

        if not horario_valido:
            raise serializers.ValidationError(
                "El veterinario no atiende en ese día y horario."
            )

        # 2. Validar solapamiento con otros turnos activos
        duracion = timedelta(minutes=servicio.duracion_estimada)
        fecha_hora_fin = fecha_hora + duracion

        solapados = Turno.objects.filter(
            veterinario=veterinario,
            estado__in=["reservado", "confirmado", "en_espera", "en_consulta"],
            fecha_hora__lt=fecha_hora_fin,
            fecha_hora__gt=fecha_hora - duracion,
        )

        if self.instance:
            solapados = solapados.exclude(pk=self.instance.pk)

        if solapados.exists():
            raise serializers.ValidationError(
                "El veterinario ya tiene un turno en ese horario."
            )

        return data


class RecetaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaItem
        fields = [
            "id",
            "consulta",
            "medicamento",
            "dosis",
            "frecuencia",
            "dias",
            "indicaciones",
        ]


class ConsultaClinicaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    veterinario_nombre = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )
    tipo_display = serializers.CharField(source="get_tipo_display", read_only=True)
    recetas = RecetaItemSerializer(many=True, read_only=True)

    class Meta:
        model = ConsultaClinica
        fields = [
            "id",
            "mascota",
            "mascota_nombre",
            "veterinario",
            "veterinario_nombre",
            "turno",
            "fecha",
            "tipo",
            "tipo_display",
            "motivo_consulta",
            "diagnostico",
            "tratamiento",
            "observaciones",
            "peso_actual",
            "temperatura",
            "frecuencia_cardiaca",
            "frecuencia_respiratoria",
            "proxima_visita",
            "recetas",
        ]


class VacunaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    veterinario_nombre = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )

    class Meta:
        model = Vacuna
        fields = [
            "id",
            "mascota",
            "mascota_nombre",
            "nombre",
            "fecha_aplicacion",
            "fecha_proxima",
            "observaciones",
            "veterinario",
            "veterinario_nombre",
        ]


class InternacionSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.CharField(source="mascota.nombre", read_only=True)
    veterinario_nombre = serializers.CharField(
        source="veterinario_responsable.nombre_completo", read_only=True
    )
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Internacion
        fields = [
            "id",
            "mascota",
            "mascota_nombre",
            "veterinario_responsable",
            "veterinario_nombre",
            "fecha_ingreso",
            "fecha_egreso",
            "motivo",
            "diagnostico_ingreso",
            "estado",
            "estado_display",
            "observaciones",
        ]


class EvolucionInternacionSerializer(serializers.ModelSerializer):
    veterinario_nombre = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )

    class Meta:
        model = EvolucionInternacion
        fields = [
            "id",
            "internacion",
            "fecha",
            "veterinario",
            "veterinario_nombre",
            "temperatura",
            "peso",
            "descripcion",
            "indicaciones",
        ]


class NotificacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source="usuario.get_full_name", read_only=True
    )

    class Meta:
        model = Notificacion
        fields = [
            "id",
            "usuario",
            "usuario_nombre",
            "tipo",
            "titulo",
            "mensaje",
            "leida",
            "fecha_lectura",
            "fecha_creacion",
        ]
