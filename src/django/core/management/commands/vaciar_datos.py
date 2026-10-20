from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from utils.limpiar_datos import vaciar_datos


class Command(BaseCommand):
    help = "Elimina los datos de la aplicación y conserva solo el administrador indicado."

    def add_arguments(self, parser):
        parser.add_argument("--administrador", required=True, help="Usuario administrador que se conserva.")
        parser.add_argument("--confirmar", action="store_true", help="Confirma la eliminación de los datos.")

    def handle(self, *args, **options):
        if not options["confirmar"]:
            raise CommandError(
                "Se eliminarán todos los datos salvo la cuenta indicada. "
                "Agregá --confirmar para ejecutar la operación."
            )
        try:
            nombre = vaciar_datos(options["administrador"])
        except User.DoesNotExist as error:
            raise CommandError("El administrador indicado no existe. No se eliminó ningún dato.") from error
        except ValueError as error:
            raise CommandError(str(error)) from error
        self.stdout.write(self.style.SUCCESS(f"Datos eliminados. Administrador conservado: {nombre}."))
