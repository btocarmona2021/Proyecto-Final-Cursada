from django.apps import AppConfig


class VeterinariaConfig(AppConfig):
    name = "veterinaria"

    def ready(self):
        from django.db.models.signals import post_migrate

        post_migrate.connect(crear_grupos_iniciales, sender=self)


def crear_grupos_iniciales(sender, **kwargs):
    from django.contrib.auth.models import Group

    for nombre in ["clientes", "veterinarios", "administradores"]:
        Group.objects.get_or_create(name=nombre)
