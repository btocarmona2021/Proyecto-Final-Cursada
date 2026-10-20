from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.db import transaction
from django.utils import timezone

from agenda.models import Servicio, Turno
from clinica.models import Veterinaria
from historia_clinica.models import ConsultaClinica, RecetaItem, Vacuna
from internaciones.models import EvolucionInternacion, Internacion
from mascotas.models import Especie, Mascota, Raza
from notificaciones.models import Notificacion
from usuarios.models import HorarioVeterinario, PerfilUsuario, VeterinarioPerfil


CUENTAS = (
    ("demo.admin", "DemoAdmin123!", "administradores", "Ana", "Demo"),
    ("demo.veterinario", "DemoVet123!", "veterinarios", "Carlos", "González"),
    ("demo.cliente1", "DemoCliente123!", "clientes", "Juan", "Pérez"),
    ("demo.cliente2", "DemoCliente123!", "clientes", "María", "López"),
    ("demo.cliente3", "DemoCliente123!", "clientes", "Santiago", "García"),
)


def fecha_local(dia, hora):
    return timezone.make_aware(datetime.combine(dia, time(hora)))


@transaction.atomic
def cargar_demo():
    hoy = timezone.localdate()
    proximo_dia = hoy + timedelta(days=1)
    while proximo_dia.isoweekday() > 5:
        proximo_dia += timedelta(days=1)
    dia_anterior = hoy - timedelta(days=1)
    while dia_anterior.isoweekday() > 5:
        dia_anterior -= timedelta(days=1)

    grupos = {
        nombre: Group.objects.get_or_create(name=nombre)[0]
        for nombre in ("administradores", "veterinarios", "clientes")
    }
    usuarios = {}
    for username, password, grupo, nombre, apellido in CUENTAS:
        email = f"{username}@example.com"
        user, creado = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": nombre,
                "last_name": apellido,
                "is_staff": grupo == "administradores",
                "is_superuser": grupo == "administradores",
            },
        )
        if creado:
            user.set_password(password)
            user.save(update_fields=["password"])
            user.groups.add(grupos[grupo])
        elif (
            user.email != email
            or not user.groups.filter(pk=grupos[grupo].pk).exists()
            or user.is_staff != (grupo == "administradores")
            or not user.is_active
        ):
            raise ValueError(f"La cuenta {username} ya existe con otra configuración.")
        usuarios[username] = user
        if grupo == "clientes":
            PerfilUsuario.objects.get_or_create(
                usuario=user,
                defaults={"telefono": "0000000000", "direccion": "Calle de ejemplo 123"},
            )

    if not Veterinaria.objects.exists():
        Veterinaria.objects.create(
            razon_social="Veterinaria de demostración",
            nombre_fantasia="VetSystem Demo",
            cuit="00-00000000-0",
            direccion="Calle de ejemplo 100",
            ciudad="Viedma",
            provincia="Río Negro",
            email="clinica@example.com",
            descripcion="Datos ficticios para la demostración del sistema.",
            horario_atencion="Lunes a viernes de 8 a 13 y de 16 a 20. Sábados de 8 a 13.",
        )

    vet, _ = VeterinarioPerfil.objects.get_or_create(
        usuario=usuarios["demo.veterinario"],
        defaults={"matricula": "DEMO-VET-001", "especialidad": "Clínica general"},
    )
    for dia in range(1, 7):
        franjas = [(8, 13)] if dia == 6 else [(8, 13), (16, 20)]
        for inicio, fin in franjas:
            HorarioVeterinario.objects.get_or_create(
                veterinario=vet, dia_semana=dia,
                hora_inicio=time(inicio), hora_fin=time(fin),
            )

    razas = {}
    for especie, emoji, nombres in (
        ("Perro", "🐶", ("Mestizo", "Labrador", "Caniche")),
        ("Gato", "🐱", ("Común europeo", "Siamés")),
        ("Conejo", "🐰", ("Mestizo",)),
    ):
        especie_obj, _ = Especie.objects.get_or_create(nombre=especie, defaults={"emoji": emoji})
        for nombre in nombres:
            razas[especie, nombre], _ = Raza.objects.get_or_create(especie=especie_obj, nombre=nombre)

    servicios = {}
    for nombre, precio, minutos in (
        ("Demo - Consulta general", "15000", 30),
        ("Demo - Vacunación", "12000", 30),
        ("Demo - Control postoperatorio", "10000", 30),
        ("Demo - Cirugía", "60000", 60),
    ):
        servicios[nombre], _ = Servicio.objects.get_or_create(
            nombre=nombre,
            defaults={"precio": Decimal(precio), "duracion_estimada": minutos,
                      "descripcion": "Servicio de demostración."},
        )

    mascotas = []
    for indice, (nombre, cliente, especie, raza, sexo, peso) in enumerate((
        ("Toby", "demo.cliente1", "Perro", "Labrador", "M", "24.5"),
        ("Luna", "demo.cliente2", "Gato", "Común europeo", "H", "4.2"),
        ("Nina", "demo.cliente3", "Perro", "Caniche", "H", "6.1"),
    ), start=1):
        mascota, _ = Mascota.objects.get_or_create(
            microchip=f"DEMO-MASCOTA-{indice:03}",
            defaults={
                "nombre": nombre, "usuario": usuarios[cliente],
                "raza": razas[especie, raza], "sexo": sexo,
                "fecha_nacimiento": hoy - timedelta(days=365 * (indice + 1)),
                "peso_actual": Decimal(peso), "observaciones": "Mascota ficticia de demostración.",
            },
        )
        mascotas.append(mascota)
        Turno.objects.get_or_create(
            notas=f"DEMO-TURNO-PROXIMO-{indice}",
            defaults={
                "mascota": mascota, "veterinario": vet,
                "servicio": servicios["Demo - Consulta general"],
                "fecha_hora": fecha_local(proximo_dia, 8 + indice),
                "estado": Turno.Estado.CONFIRMADO if indice == 1 else Turno.Estado.RESERVADO,
                "motivo_consulta": "Control general de demostración", "creado_por_cliente": True,
            },
        )
        Notificacion.objects.get_or_create(
            usuario=usuarios[cliente], titulo="Bienvenido a la demostración",
            defaults={"tipo": Notificacion.Tipo.SISTEMA,
                      "mensaje": "Tu mascota y un turno de ejemplo ya están cargados."},
        )

    for indice, mascota in enumerate(mascotas[:2], start=1):
        turno, _ = Turno.objects.get_or_create(
            notas=f"DEMO-TURNO-ATENDIDO-{indice}",
            defaults={
                "mascota": mascota, "veterinario": vet,
                "servicio": servicios["Demo - Consulta general"],
                "fecha_hora": fecha_local(dia_anterior, 8 + indice),
                "estado": Turno.Estado.ATENDIDO, "motivo_consulta": "Control de rutina",
            },
        )
        consulta, _ = ConsultaClinica.objects.get_or_create(
            turno=turno,
            defaults={
                "mascota": mascota, "veterinario": vet, "fecha": turno.fecha_hora,
                "motivo_consulta": "Control de rutina", "diagnostico": "Control general sin hallazgos.",
                "tratamiento": "Seguimiento preventivo.", "peso_actual": mascota.peso_actual,
                "temperatura": Decimal("38.5"), "proxima_visita": proximo_dia,
            },
        )
        RecetaItem.objects.get_or_create(
            consulta=consulta, medicamento="Producto ficticio de demostración",
            defaults={"dosis": "Sin uso clínico", "indicaciones": "Registro de ejemplo; no es una prescripción real."},
        )

    for mascota in mascotas:
        Vacuna.objects.get_or_create(
            mascota=mascota, nombre="Vacuna de ejemplo",
            defaults={"fecha_aplicacion": dia_anterior, "fecha_proxima": hoy + timedelta(days=365),
                      "veterinario": vet, "observaciones": "Registro ficticio."},
        )

    for indice, mascota in enumerate((mascotas[0], mascotas[2]), start=1):
        internacion, _ = Internacion.objects.get_or_create(
            mascota=mascota, motivo=f"DEMO - Observación {indice}",
            defaults={
                "veterinario_responsable": vet, "fecha_ingreso": fecha_local(dia_anterior, 11),
                "estado": Internacion.Estado.OBSERVACION if indice == 1 else Internacion.Estado.ALTA,
                "fecha_egreso": fecha_local(dia_anterior, 12) if indice == 2 else None,
                "diagnostico_ingreso": "Seguimiento de demostración.",
            },
        )
        EvolucionInternacion.objects.get_or_create(
            internacion=internacion, descripcion="Evolución de ejemplo: paciente estable.",
            defaults={"veterinario": vet, "fecha": internacion.fecha_ingreso,
                      "temperatura": Decimal("38.4"), "peso": mascota.peso_actual},
        )

    return usuarios
