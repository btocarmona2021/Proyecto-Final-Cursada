from django.test import TestCase
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient
from unittest.mock import patch
from usuarios.models import PerfilUsuario, VeterinarioPerfil
from usuarios.serializers import ClienteRegistroSerializer, VeterinarioRegistroSerializer


class RegistroUsuariosTests(TestCase):
    def test_admin_registra_veterinario_con_datos_completos(self):
        admin = User.objects.create_user(username='administrador', is_staff=True)
        cliente = APIClient()
        cliente.force_authenticate(admin)
        respuesta = cliente.post('/api/veterinarios/', {
            'username': 'vet_nuevo', 'password': 'ClaveDePrueba123!',
            'first_name': 'Ana', 'last_name': 'Pérez', 'email': 'ana@example.com',
            'matricula': 'MAT-001', 'especialidad': 'Clínica general',
        }, format='json')
        self.assertEqual(respuesta.status_code, 201, respuesta.data)
        usuario = User.objects.get(username='vet_nuevo')
        self.assertEqual(usuario.get_full_name(), 'Ana Pérez')
        self.assertEqual(usuario.email, 'ana@example.com')
        self.assertTrue(usuario.check_password('ClaveDePrueba123!'))
        self.assertTrue(usuario.groups.filter(name='veterinarios').exists())
        self.assertTrue(VeterinarioPerfil.objects.filter(usuario=usuario, matricula='MAT-001').exists())

    def test_veterinario_consulta_clientes_pero_no_cuentas_ni_alta_de_veterinarios(self):
        vet = User.objects.create_user(username='vet')
        grupo, _ = Group.objects.get_or_create(name='veterinarios')
        vet.groups.add(grupo)
        dueno = User.objects.create_user(username='cliente')
        PerfilUsuario.objects.create(usuario=dueno)
        cliente = APIClient()
        cliente.force_authenticate(vet)
        respuesta = cliente.get('/api/clientes/')
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data[0]['usuario']['id'], dueno.id)
        self.assertEqual(cliente.get('/api/usuarios/').status_code, 403)
        self.assertEqual(cliente.post('/api/veterinarios/', {}, format='json').status_code, 403)

    def test_matricula_repetida_no_crea_otra_cuenta(self):
        usuario = User.objects.create_user(username='vet_existente', password='ClaveDePrueba123!')
        VeterinarioPerfil.objects.create(usuario=usuario, matricula='MAT-001')
        serializer = VeterinarioRegistroSerializer(data={
            'username': 'vet_nuevo', 'password': 'ClaveDePrueba123!',
            'first_name': 'Ana', 'last_name': 'Pérez',
            'email': 'ana@example.com', 'matricula': 'MAT-001',
        })
        self.assertFalse(serializer.is_valid())
        self.assertIn('matricula', serializer.errors)
        self.assertFalse(User.objects.filter(username='vet_nuevo').exists())

    def test_fallo_del_perfil_revierte_el_registro_completo(self):
        for serializer_class, modelo, extra in (
            (ClienteRegistroSerializer, PerfilUsuario, {}),
            (VeterinarioRegistroSerializer, VeterinarioPerfil, {'matricula': 'MAT-002'}),
        ):
            with self.subTest(serializer=serializer_class.__name__):
                serializer = serializer_class(data={
                    'username': 'registro_fallido', 'password': 'ClaveDePrueba123!', **extra,
                })
                self.assertTrue(serializer.is_valid(), serializer.errors)
                with patch.object(modelo.objects, 'create', side_effect=RuntimeError('Fallo de prueba')):
                    with self.assertRaises(RuntimeError):
                        serializer.save()
                self.assertFalse(User.objects.filter(username='registro_fallido').exists())
