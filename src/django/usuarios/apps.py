# usuarios/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate


def crear_grupos_iniciales(sender, **kwargs):
    """
    Crea los grupos básicos del sistema si no existen.
    Se ejecuta al final de migrate para esta app.
    """
    from django.contrib.auth.models import Group

    for nombre in ["clientes", "veterinarios", "administradores"]:
        Group.objects.get_or_create(name=nombre)


class UsuariosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "usuarios"

    def ready(self):
        # Conectar la señal post_migrate para esta app
        post_migrate.connect(crear_grupos_iniciales, sender=self)