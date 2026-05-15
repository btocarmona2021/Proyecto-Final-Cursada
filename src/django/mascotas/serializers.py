# mascotas/serializers.py
from rest_framework import serializers
from .models import Especie, Raza, Mascota
from django.contrib.auth.models import User


# SERIALIZER PARA ESPECIE
class EspecieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especie
        fields = [
            "id",
            "nombre",
            "emoji",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# SERIALIZER PARA RAZA
class RazaSerializer(serializers.ModelSerializer):
    especie = EspecieSerializer(read_only=True)
    especie_id = serializers.PrimaryKeyRelatedField(
        source="especie", 
        queryset=Especie.objects.all(), 
        write_only=True
    )

    class Meta:
        model = Raza
        fields = [
            "id",
            "especie",
            "especie_id",
            "nombre",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


# SERIALIZER PARA CREACIÓN DE MASCOTA
class MascotaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear mascotas - más simple"""
    
    class Meta:
        model = Mascota
        fields = [
            "id",
            "nombre",
            "raza",
            "fecha_nacimiento",
            "sexo",
            "color",
            "peso_actual",
            "microchip",
            "foto",
            "usuario",
        ]
        read_only_fields = ["id"]
    
    def validate(self, data):
        # Verificar que el usuario sea del grupo Cliente
        usuario = data.get('usuario')
        if usuario and not usuario.groups.filter(name='clientes').exists():
            raise serializers.ValidationError(
                "Solo los usuarios del grupo 'clientes' pueden ser dueños de mascotas"
            )
        return data


# SERIALIZER PARA LECTURA DE MASCOTA (completo con info)
class MascotaSerializer(serializers.ModelSerializer):
    raza_info = RazaSerializer(source='raza', read_only=True)
    raza_nombre = serializers.SerializerMethodField()
    especie_nombre = serializers.SerializerMethodField()
    usuario_info = serializers.SerializerMethodField()
    usuario_nombre = serializers.SerializerMethodField()
    sexo_display = serializers.CharField(source='get_sexo_display', read_only=True)
    edad_anos = serializers.SerializerMethodField()

    class Meta:
        model = Mascota
        fields = [
            "id",
            "nombre",
            "raza",
            "raza_info",
            "raza_nombre",
            "especie_nombre",
            "fecha_nacimiento",
            "edad_anos",
            "sexo",
            "sexo_display",
            "color",
            "peso_actual",
            "microchip",
            "foto",
            "usuario",
            "usuario_info",
            "usuario_nombre",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = [
            "id",
            "raza_info",
            "raza_nombre",
            "especie_nombre",
            "usuario_info",
            "usuario_nombre",
            "sexo_display",
            "edad_anos",
            "created_at",
            "updated_at",
        ]

    def get_raza_nombre(self, obj):
        return obj.raza.nombre if obj.raza else None

    def get_especie_nombre(self, obj):
        return obj.raza.especie.nombre if obj.raza and obj.raza.especie else None

    def get_usuario_nombre(self, obj):
        if obj.usuario:
            return f"{obj.usuario.last_name}, {obj.usuario.first_name}".strip()
        return None
    
    def get_usuario_info(self, obj):
        """Información completa del dueño"""
        if obj.usuario:
            return {
                "id": obj.usuario.id,
                "username": obj.usuario.username,
                "nombre_completo": f"{obj.usuario.first_name} {obj.usuario.last_name}".strip(),
                "email": obj.usuario.email,
            }
        return None
    
    def get_edad_anos(self, obj):
        """Calcular edad en años"""
        if obj.fecha_nacimiento:
            from datetime import date
            today = date.today()
            edad = today.year - obj.fecha_nacimiento.year
            if today.month < obj.fecha_nacimiento.month or \
               (today.month == obj.fecha_nacimiento.month and today.day < obj.fecha_nacimiento.day):
                edad -= 1
            return edad
        return None