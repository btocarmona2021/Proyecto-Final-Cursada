from rest_framework import serializers
from django.utils import timezone
from .models import Notificacion


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = "__all__"
        read_only_fields = [
            "id",
            "fecha_lectura",  # ✅ AUTO-SETEADA
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        # ✅ Si se marca como leída y antes no estaba leída
        if validated_data.get('leida') and not instance.leida:
            validated_data['fecha_lectura'] = timezone.now()
        
        # ✅ Si se desmarca como leída, limpiar fecha
        if not validated_data.get('leida', instance.leida):
            validated_data['fecha_lectura'] = None
        
        return super().update(instance, validated_data)