from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .models import PerfilUsuario, VeterinarioPerfil, HorarioVeterinario


# SERIALIZER PARA USUARIO (solo lectura)
class UsuarioSerializer(serializers.ModelSerializer):
    grupo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "grupo"]

    def get_grupo(self, obj):
        first_group = obj.groups.first()
        return first_group.name if first_group else None


# SERIALIZER PARA REGISTRO DE CLIENTE
class ClienteRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    telefono = serializers.CharField(required=False, allow_blank=True)
    direccion = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "telefono",
            "direccion",
        ]
        read_only_fields = ["id"]
    
    def create(self, validated_data):
        telefono = validated_data.pop('telefono', '')
        direccion = validated_data.pop('direccion', '')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        grupo, _ = Group.objects.get_or_create(name='clientes')
        user.groups.add(grupo)
        
        PerfilUsuario.objects.create(
            usuario=user,
            telefono=telefono,
            direccion=direccion
        )
        
        return user


# SERIALIZER PARA REGISTRO DE VETERINARIO
class VeterinarioRegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    matricula = serializers.CharField(required=True)
    especialidad = serializers.CharField(required=False, allow_blank=True)
    biografia = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "matricula",
            "especialidad",
            "biografia",
        ]
        read_only_fields = ["id"]
    
    def create(self, validated_data):
        matricula = validated_data.pop('matricula')
        especialidad = validated_data.pop('especialidad', '')
        biografia = validated_data.pop('biografia', '')
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        grupo, _ = Group.objects.get_or_create(name='veterinarios')
        user.groups.add(grupo)
        
        VeterinarioPerfil.objects.create(
            usuario=user,
            matricula=matricula,
            especialidad=especialidad,
            biografia=biografia
        )
        
        return user


# SERIALIZER PARA PERFIL USUARIO (edición)
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = PerfilUsuario
        fields = [
            "id",
            "usuario",
            "telefono",
            "direccion",
            "foto",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = [
            "id",
            "usuario",
            "fecha_creacion",
            "fecha_actualizacion",
        ]


# SERIALIZER PARA PERFIL DE VETERINARIO (edición)
class VeterinarioPerfilSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    
    class Meta:
        model = VeterinarioPerfil
        fields = [
            "id",
            "usuario",
            "matricula",
            "especialidad",
            "biografia",
            "foto",
            "disponible",
            "fecha_creacion",
            "fecha_actualizacion",
        ]
        read_only_fields = [
            "id",
            "usuario",
            "fecha_creacion",
            "fecha_actualizacion",
        ]


# SERIALIZER PARA HORARIO DE VETERINARIO
class HorarioVeterinarioSerializer(serializers.ModelSerializer):
    dia_semana_display = serializers.CharField(
        source="get_dia_semana_display", read_only=True
    )
    nombre_veterinario = serializers.CharField(
        source="veterinario.nombre_completo", read_only=True
    )
    veterinario_id = serializers.IntegerField(source="veterinario.id")

    class Meta:
        model = HorarioVeterinario
        fields = [
            "id",
            "veterinario_id",
            "nombre_veterinario",
            "dia_semana",
            "dia_semana_display",
            "hora_inicio",
            "hora_fin",
            "created_at",
            "updated_at",
            "activo",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "nombre_veterinario", "dia_semana_display"]

    def create(self, validated_data):
        veterinario_data = validated_data.pop('veterinario')
        veterinario = VeterinarioPerfil.objects.get(id=veterinario_data['id'])
        return HorarioVeterinario.objects.create(veterinario=veterinario, **validated_data)

    def update(self, instance, validated_data):
        if 'veterinario' in validated_data:
            veterinario_data = validated_data.pop('veterinario')
            instance.veterinario = VeterinarioPerfil.objects.get(id=veterinario_data['id'])
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        veterinario_data = data.get("veterinario")
        if veterinario_data:
            veterinario = VeterinarioPerfil.objects.get(id=veterinario_data['id'])
        else:
            veterinario = getattr(self.instance, "veterinario", None)
        
        dia_semana = data.get("dia_semana", getattr(self.instance, "dia_semana", None))
        hora_inicio = data.get("hora_inicio", getattr(self.instance, "hora_inicio", None))
        hora_fin = data.get("hora_fin", getattr(self.instance, "hora_fin", None))

        solapados = HorarioVeterinario.objects.filter(
            veterinario=veterinario,
            dia_semana=dia_semana,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )

        if self.instance:
            solapados = solapados.exclude(pk=self.instance.pk)

        if solapados.exists():
            raise serializers.ValidationError(
                "El horario se solapa con un horario existente para ese día."
            )

        return data