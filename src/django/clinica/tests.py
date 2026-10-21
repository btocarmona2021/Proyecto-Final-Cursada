from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from clinica.models import Veterinaria


class DatosClinicaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(username='admin_clinica', is_staff=True)
        cls.usuario = User.objects.create_user(username='usuario_clinica')

    def setUp(self):
        self.api = APIClient()
        self.datos = {
            'razon_social': 'Clínica de prueba', 'nombre_fantasia': 'Vet Prueba',
            'cuit': '20-11111111-1', 'direccion': 'Calle de prueba 100',
            'ciudad': 'Viedma', 'provincia': 'Río Negro',
        }

    def test_consulta_publica_no_exige_login(self):
        Veterinaria.objects.create(**self.datos)
        respuesta = self.api.get('/api/veterinaria/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data[0]['nombre_fantasia'], 'Vet Prueba')

    def test_solo_administrador_puede_guardar(self):
        self.assertEqual(self.api.post('/api/veterinaria/', self.datos, format='json').status_code, 401)
        self.api.force_authenticate(self.usuario)
        self.assertEqual(self.api.post('/api/veterinaria/', self.datos, format='json').status_code, 403)
        self.assertFalse(Veterinaria.objects.exists())

    def test_registro_y_edicion_conservan_la_misma_clinica(self):
        self.api.force_authenticate(self.admin)
        respuesta = self.api.post('/api/veterinaria/', {**self.datos, 'sitio_web': 'https://example.com'}, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        identificador = respuesta.data['id']
        respuesta = self.api.put(f'/api/veterinaria/{identificador}/', {
            **self.datos, 'telefono': '02920123456', 'descripcion': 'Descripción actualizada',
        }, format='json')
        self.assertEqual(respuesta.status_code, 200, respuesta.data)
        self.assertEqual(Veterinaria.objects.count(), 1)
        clinica = Veterinaria.objects.get(pk=identificador)
        self.assertEqual(clinica.telefono, '02920123456')
        self.assertEqual(clinica.sitio_web, 'https://example.com')

    def test_segunda_clinica_devuelve_error_de_validacion(self):
        Veterinaria.objects.create(**self.datos)
        self.api.force_authenticate(self.admin)
        respuesta = self.api.post('/api/veterinaria/', {**self.datos, 'cuit': '20-22222222-2'}, format='json')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('non_field_errors', respuesta.data)
        self.assertEqual(Veterinaria.objects.count(), 1)
