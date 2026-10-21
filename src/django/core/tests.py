from django.test import TestCase
from django.contrib.auth.models import Group, User
from django.utils import timezone
from datetime import time, timedelta
from rest_framework.test import APIClient

from agenda.models import Servicio, Turno
from historia_clinica.models import ConsultaClinica, Vacuna
from internaciones.models import Internacion
from mascotas.models import Especie, Mascota, Raza
from notificaciones.models import Notificacion
from usuarios.models import HorarioVeterinario, PerfilUsuario, VeterinarioPerfil


class CircuitoPorRolesTests(TestCase):
    """Datos de prueba aislados; nunca cargar ni vaciar la base de la aplicación."""

    @classmethod
    def setUpTestData(cls):
        clientes, _ = Group.objects.get_or_create(name='clientes')
        veterinarios, _ = Group.objects.get_or_create(name='veterinarios')
        cls.admin = User.objects.create_user(username='admin_prueba', is_staff=True)
        cls.cliente = User.objects.create_user(username='cliente_prueba')
        cls.otro = User.objects.create_user(username='otro_cliente')
        for usuario in (cls.cliente, cls.otro):
            usuario.groups.add(clientes)
            PerfilUsuario.objects.create(usuario=usuario)
        cls.vet = User.objects.create_user(username='vet_prueba')
        cls.vet.groups.add(veterinarios)
        cls.perfil_vet = VeterinarioPerfil.objects.create(usuario=cls.vet, matricula='PRUEBA-001')
        especie = Especie.objects.create(nombre='Perro')
        cls.raza = Raza.objects.create(nombre='Mestizo', especie=especie)
        cls.mascota = Mascota.objects.create(nombre='Toby', sexo='M', usuario=cls.cliente, raza=cls.raza)
        cls.ajena = Mascota.objects.create(nombre='Luna', sexo='H', usuario=cls.otro, raza=cls.raza)
        cls.servicio = Servicio.objects.create(nombre='Control', duracion_estimada=30)
        cls.fecha = timezone.localtime(timezone.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        HorarioVeterinario.objects.create(
            veterinario=cls.perfil_vet, dia_semana=cls.fecha.isoweekday(),
            hora_inicio=time(8), hora_fin=time(20),
        )
        for mascota, hora in ((cls.mascota, 9), (cls.ajena, 11)):
            turno = Turno.objects.create(
                mascota=mascota, veterinario=cls.perfil_vet, servicio=cls.servicio,
                fecha_hora=cls.fecha.replace(hour=hora),
            )
            if mascota == cls.mascota:
                cls.turno = turno
            ConsultaClinica.objects.create(mascota=mascota, veterinario=cls.perfil_vet)
            Vacuna.objects.create(mascota=mascota, nombre='Ejemplo', fecha_aplicacion=timezone.localdate(), fecha_proxima=timezone.localdate() + timedelta(days=30))
            Internacion.objects.create(mascota=mascota, veterinario_responsable=cls.perfil_vet, motivo='Observación')
            Notificacion.objects.create(usuario=mascota.usuario, tipo='sistema', titulo='Ejemplo', mensaje='Prueba')

    def setUp(self):
        self.api = APIClient()

    def test_endpoints_privados_exigen_autenticacion(self):
        for ruta in ('usuarios', 'clientes', 'veterinarios', 'mascotas', 'turnos', 'consultas', 'vacunas', 'internaciones', 'notificaciones', 'horarios'):
            with self.subTest(ruta=ruta):
                self.assertEqual(self.api.get(f'/api/{ruta}/').status_code, 401)

    def test_cliente_solo_consulta_sus_registros(self):
        self.api.force_authenticate(self.cliente)
        for ruta in ('clientes', 'mascotas', 'turnos', 'consultas', 'vacunas', 'internaciones', 'notificaciones'):
            with self.subTest(ruta=ruta):
                respuesta = self.api.get(f'/api/{ruta}/')
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(len(respuesta.data), 1)
        self.assertEqual(self.api.get(f'/api/mascotas/{self.ajena.pk}/').status_code, 404)

    def test_cliente_reserva_para_su_mascota_y_no_para_otra(self):
        self.api.force_authenticate(self.cliente)
        datos = {
            'mascota': self.mascota.pk, 'veterinario': self.perfil_vet.pk,
            'servicio': self.servicio.pk, 'fecha_hora': self.fecha.isoformat(), 'urgencia': False,
        }
        respuesta = self.api.post('/api/turnos/', datos, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        self.assertTrue(Turno.objects.get(pk=respuesta.data['id']).creado_por_cliente)
        datos['mascota'] = self.ajena.pk
        datos['fecha_hora'] = self.fecha.replace(hour=13).isoformat()
        self.assertEqual(self.api.post('/api/turnos/', datos, format='json').status_code, 403)

    def test_cliente_cancela_pero_no_edita_ni_elimina_turnos(self):
        self.api.force_authenticate(self.cliente)
        ruta = f'/api/turnos/{self.turno.pk}/'
        self.assertEqual(self.api.patch(ruta, {'estado': 'atendido'}, format='json').status_code, 403)
        self.assertEqual(self.api.delete(ruta).status_code, 403)
        self.assertEqual(self.api.post(ruta + 'cancelar/').status_code, 200)
        self.turno.refresh_from_db()
        self.assertEqual(self.turno.estado, 'cancelado')

    def test_cliente_no_registra_atencion_ni_catalogos(self):
        self.api.force_authenticate(self.cliente)
        for ruta in ('mascotas', 'consultas', 'recetas', 'vacunas', 'internaciones', 'evoluciones-internacion', 'servicios', 'especies', 'horarios', 'veterinarios'):
            with self.subTest(ruta=ruta):
                self.assertEqual(self.api.post(f'/api/{ruta}/', {}, format='json').status_code, 403)

    def test_veterinario_consulta_duenos_y_registra_atencion(self):
        self.api.force_authenticate(self.vet)
        respuesta = self.api.get('/api/clientes/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(len(respuesta.data), 2)
        self.assertEqual(self.api.get('/api/usuarios/').status_code, 403)
        perfil = PerfilUsuario.objects.get(usuario=self.cliente)
        self.assertEqual(self.api.patch(f'/api/clientes/{perfil.pk}/', {'telefono': '123'}, format='json').status_code, 403)
        self.assertEqual(self.api.post(f'/api/turnos/{self.turno.pk}/atender/').status_code, 200)
        respuesta = self.api.post('/api/consultas/', {
            'mascota': self.mascota.pk, 'veterinario': self.perfil_vet.pk,
            'turno': self.turno.pk, 'diagnostico': 'Control de prueba',
        }, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        receta = self.api.post('/api/recetas/', {
            'consulta': respuesta.data['id'], 'medicamento': 'Producto ficticio', 'dosis': 'Sin uso clínico',
        }, format='json')
        self.assertEqual(receta.status_code, 201, receta.data)

    def test_fecha_de_vacuna_se_conserva_en_la_api(self):
        self.api.force_authenticate(self.cliente)
        respuesta = self.api.get('/api/vacunas/')
        self.assertEqual(respuesta.data[0]['fecha_aplicacion'], timezone.localdate().isoformat())
        self.assertEqual(respuesta.data[0]['fecha_proxima'], (timezone.localdate() + timedelta(days=30)).isoformat())

    def test_admin_consulta_usuarios_y_todos_los_duenos(self):
        self.api.force_authenticate(self.admin)
        self.assertEqual(self.api.get('/api/usuarios/').status_code, 200)
        self.assertEqual(len(self.api.get('/api/clientes/').data), 2)

    def test_receta_se_edita_y_elimina_desde_consulta(self):
        consulta = ConsultaClinica.objects.get(mascota=self.mascota)
        self.api.force_authenticate(self.vet)
        datos = {'consulta': consulta.pk, 'medicamento': 'Producto ficticio', 'dosis': 'Dato de prueba', 'frecuencia': 'Texto de prueba', 'dias': 3, 'indicaciones': 'Sin uso clínico'}
        respuesta = self.api.post('/api/recetas/', datos, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        ruta = f"/api/recetas/{respuesta.data['id']}/"
        self.api.force_authenticate(self.admin)
        respuesta = self.api.put(ruta, {**datos, 'dosis': 'Texto corregido', 'dias': None}, format='json')
        self.assertEqual(respuesta.status_code, 200, respuesta.data)
        self.assertIsNone(respuesta.data['dias'])
        respuesta = self.api.get(f'/api/consultas/{consulta.pk}/')
        self.assertEqual(respuesta.data['recetas'][0]['dosis'], 'Texto corregido')
        self.assertEqual(self.api.delete(ruta).status_code, 204)
        self.assertEqual(self.api.get(f'/api/consultas/{consulta.pk}/').data['recetas'], [])

    def test_cliente_ve_receta_propia_sin_poder_modificar_ni_ver_consulta_ajena(self):
        from historia_clinica.models import RecetaItem
        consulta = ConsultaClinica.objects.get(mascota=self.mascota)
        ajena = ConsultaClinica.objects.get(mascota=self.ajena)
        receta = RecetaItem.objects.create(consulta=consulta, medicamento='Producto ficticio', dosis='Prueba propia')
        RecetaItem.objects.create(consulta=ajena, medicamento='Otro producto', dosis='Prueba ajena')
        self.api.force_authenticate(self.cliente)
        respuesta = self.api.get('/api/consultas/')
        self.assertEqual(len(respuesta.data), 1)
        self.assertEqual(respuesta.data[0]['recetas'][0]['id'], receta.pk)
        self.assertEqual(self.api.get(f'/api/consultas/{ajena.pk}/').status_code, 404)
        self.assertEqual(self.api.post('/api/recetas/', {'consulta': consulta.pk, 'medicamento': 'Prueba', 'dosis': 'Prueba'}, format='json').status_code, 403)
        self.assertEqual(self.api.patch(f'/api/recetas/{receta.pk}/', {'dosis': 'Cambio'}, format='json').status_code, 403)
        self.assertEqual(self.api.delete(f'/api/recetas/{receta.pk}/').status_code, 403)
