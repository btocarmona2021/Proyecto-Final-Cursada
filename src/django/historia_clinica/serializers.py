from rest_framework import serializers
from .models import ConsultaClinica, RecetaItem, Vacuna


# SERIALIZER PARA RECETAITEM
class RecetaItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaItem
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


# SERIALIZER PARA CONSULTA CLINICA
class ConsultaClinicaSerializer(serializers.ModelSerializer):
    mascota_nombre = serializers.SerializerMethodField()
    veterinario_nombre = serializers.SerializerMethodField()
    tipo_display = serializers.SerializerMethodField()
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
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = [
            "id",
            "mascota_nombre",
            "veterinario_nombre",
            "tipo_display",
            "recetas",
            "created_at",
            "updated_at",
        ]

    def get_mascota_nombre(self, obj):
        return obj.mascota.nombre if obj.mascota_id else None

    def get_veterinario_nombre(self, obj):
        if obj.veterinario_id:
            u = obj.veterinario.usuario
            return f"{u.last_name}, {u.first_name}".strip()
        return None

    def get_tipo_display(self, obj):
        return obj.get_tipo_display()


# SERIALIZER PARA VACUNA
class VacunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacuna
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]