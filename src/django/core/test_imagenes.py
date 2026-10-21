from io import BytesIO
from tempfile import TemporaryDirectory
from PIL import Image
from django.contrib.auth.models import Group, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.test import APIClient
from core.imagenes import ImagenValidada
from rest_framework.exceptions import ValidationError
from usuarios.models import PerfilUsuario
from mascotas.models import Especie, Raza


def imagen(formato='PNG'):
    contenido = BytesIO()
    Image.new('RGB', (8, 8), 'green').save(contenido, formato)
    return SimpleUploadedFile('foto.' + formato.lower(), contenido.getvalue(), content_type='image/' + formato.lower())


class CargaImagenesTests(TestCase):
    def setUp(self):
        carpeta = TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        ajustes = override_settings(MEDIA_ROOT=carpeta.name)
        ajustes.enable()
        self.addCleanup(ajustes.disable)
        self.api = APIClient()
        self.admin = User.objects.create_user(username='admin_imagen', is_staff=True)
        self.api.force_authenticate(self.admin)

    def test_logo_multipart_se_guarda_y_editar_texto_lo_conserva(self):
        datos = dict(razon_social='Clínica', cuit='20-11111111-1', direccion='Calle 1', ciudad='Viedma', provincia='Río Negro')
        respuesta = self.api.post('/api/veterinaria/', {**datos, 'logo': imagen()}, format='multipart')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        logo = respuesta.data['logo']
        self.assertIn('/media/veterinaria/', logo)
        respuesta = self.api.put(f"/api/veterinaria/{respuesta.data['id']}/", {**datos, 'telefono': '123'}, format='json')
        self.assertEqual(respuesta.status_code, 200, respuesta.data)
        self.assertEqual(respuesta.data['logo'], logo)

    def test_registro_de_cliente_y_veterinario_con_foto(self):
        for ruta, extra in (('clientes', {}), ('veterinarios', {'matricula': 'FOTO-01'})):
            respuesta = self.api.post(f'/api/{ruta}/', {
                'username': 'foto_' + ruta, 'password': 'Prueba123!',
                'first_name': 'Ana', 'last_name': 'Prueba', 'email': 'foto@example.com',
                'foto': imagen(), **extra,
            }, format='multipart')
            self.assertEqual(respuesta.status_code, 201, respuesta.data)
            self.assertIn('/media/perfiles/', respuesta.data['foto'])
            foto_anterior = respuesta.data['foto'].split('/media/')[1]
            respuesta = self.api.patch(f"/api/{ruta}/{respuesta.data['id']}/", {'foto': imagen('JPEG')}, format='multipart')
            self.assertEqual(respuesta.status_code, 200, respuesta.data)
            self.assertNotEqual(respuesta.data['foto'].split('/media/')[1], foto_anterior)

    def test_mascota_con_foto_y_edicion_sin_reemplazar(self):
        dueno = User.objects.create_user(username='dueno_foto')
        grupo, _ = Group.objects.get_or_create(name='clientes')
        dueno.groups.add(grupo)
        PerfilUsuario.objects.create(usuario=dueno)
        raza = Raza.objects.create(nombre='Mestizo', especie=Especie.objects.create(nombre='Perro'))
        datos = {'nombre': 'Toby', 'usuario': dueno.id, 'raza': raza.id, 'sexo': 'M'}
        respuesta = self.api.post('/api/mascotas/', {**datos, 'foto': imagen()}, format='multipart')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        foto = respuesta.data['foto']
        respuesta = self.api.put(f"/api/mascotas/{respuesta.data['id']}/", {**datos, 'color': 'Blanco'}, format='json')
        self.assertEqual(respuesta.status_code, 200, respuesta.data)
        self.assertEqual(respuesta.data['foto'], foto)

    def test_rechaza_archivo_falso_formato_no_admitido_y_exceso(self):
        for archivo in (
            SimpleUploadedFile('falsa.png', b'no es una imagen', content_type='image/png'),
            imagen('GIF'),
            SimpleUploadedFile('grande.png', b'0' * (5 * 1024 * 1024 + 1), content_type='image/png'),
        ):
            with self.subTest(nombre=archivo.name), self.assertRaises((ValidationError, DjangoValidationError)):
                ImagenValidada().run_validation(archivo)

    def test_imagen_invalida_no_crea_usuario(self):
        respuesta = self.api.post('/api/clientes/', {'username': 'foto_invalida', 'password': 'Prueba123!',
            'foto': SimpleUploadedFile('falsa.png', b'error', content_type='image/png')}, format='multipart')
        self.assertEqual(respuesta.status_code, 400)
        self.assertIn('foto', respuesta.data)
        self.assertFalse(User.objects.filter(username='foto_invalida').exists())
