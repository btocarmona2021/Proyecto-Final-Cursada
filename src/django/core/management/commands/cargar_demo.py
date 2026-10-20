from django.core.management.base import BaseCommand, CommandError

from utils.datos_demo import CUENTAS, cargar_demo


class Command(BaseCommand):
    help = "Carga cuentas y datos ficticios para demostrar el sistema."

    def handle(self, *args, **options):
        try:
            cargar_demo()
        except ValueError as error:
            raise CommandError(str(error)) from error
        self.stdout.write(self.style.SUCCESS("Datos de demostración disponibles."))
        self.stdout.write("Credenciales iniciales (no se restablecen contraseñas existentes):")
        for username, password, grupo, _, _ in CUENTAS:
            self.stdout.write(f"{grupo}: {username} / {password}")
