from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, Auditoria

Usuario = get_user_model()


class UsuarioModelTest(TestCase):
    """Tests para el modelo Usuario personalizado"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario_data = {
            'username': 'matrona_test',
            'rut': '12.345.678-5',
            'first_name': 'Ana',
            'last_name': 'González',
            'email': 'ana@hospital.cl',
            'rol': 'matrona',
            'password': 'testpass123'
        }
    
    def test_crear_usuario(self):
        """Test creación de usuario"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertEqual(usuario.username, 'matrona_test')
        self.assertEqual(usuario.rut, '12.345.678-5')
        self.assertEqual(usuario.rol, 'matrona')
        self.assertTrue(usuario.is_active)
    
    def test_nombre_completo_property(self):
        """Test del método nombre_completo"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertEqual(usuario.nombre_completo, 'Ana González')
    
    def test_puede_registrar_parto_matrona(self):
        """Test que matrona puede registrar partos"""
        self.usuario_data['rol'] = 'matrona'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_registrar_parto())
    
    def test_puede_registrar_parto_medico(self):
        """Test que médico obstetra puede registrar partos"""
        self.usuario_data['rol'] = 'medico_obstetra'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_registrar_parto())
    
    def test_no_puede_registrar_parto_pediatra(self):
        """Test que pediatra NO puede registrar partos"""
        self.usuario_data['rol'] = 'pediatra'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertFalse(usuario.puede_registrar_parto())
    
    def test_puede_evaluar_rn_pediatra(self):
        """Test que pediatra puede evaluar recién nacidos"""
        self.usuario_data['rol'] = 'pediatra'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_evaluar_rn())
    
    def test_puede_evaluar_rn_enfermera_neonatal(self):
        """Test que enfermera neonatal puede evaluar RN"""
        self.usuario_data['rol'] = 'enfermera_neonatal'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_evaluar_rn())
    
    def test_puede_ver_datos_sensibles_jefe(self):
        """Test que jefe de servicio puede ver datos sensibles"""
        self.usuario_data['rol'] = 'jefe_servicio'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_ver_datos_sensibles())
    
    def test_puede_generar_reportes_jefe(self):
        """Test que jefe de servicio puede generar reportes"""
        self.usuario_data['rol'] = 'jefe_servicio'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_generar_reportes())
    
    def test_puede_gestionar_usuarios_super_admin(self):
        """Test que super admin puede gestionar usuarios"""
        self.usuario_data['rol'] = 'super_admin'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertTrue(usuario.puede_gestionar_usuarios())
    
    def test_no_puede_gestionar_usuarios_matrona(self):
        """Test que matrona NO puede gestionar usuarios"""
        self.usuario_data['rol'] = 'matrona'
        usuario = Usuario.objects.create_user(**self.usuario_data)
        self.assertFalse(usuario.puede_gestionar_usuarios())
    
    def test_bloquear_cuenta(self):
        """Test bloqueo de cuenta"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        usuario.bloquear_cuenta()
        self.assertFalse(usuario.activo)  # Usar campo activo personalizado
        self.assertTrue(usuario.cuenta_bloqueada)
    
    def test_desbloquear_cuenta(self):
        """Test desbloqueo de cuenta"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        usuario.bloquear_cuenta()
        usuario.desbloquear_cuenta()
        self.assertTrue(usuario.activo)  # Usar campo activo personalizado
        self.assertFalse(usuario.cuenta_bloqueada)
    
    def test_registrar_acceso(self):
        """Test registro de acceso exitoso resetea intentos fallidos"""
        usuario = Usuario.objects.create_user(**self.usuario_data)
        # Simular intentos fallidos
        usuario.intentos_fallidos = 3
        usuario.save()
        
        # Registrar acceso exitoso
        usuario.registrar_acceso()
        
        # Verificar que se resetearon los intentos fallidos
        self.assertEqual(usuario.intentos_fallidos, 0)


class LoginViewTest(TestCase):
    """Tests para la vista de login - Simplificados"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            rut='12.345.678-5',
            password='testpass123',
            rol='matrona'
        )
    
    def test_autenticacion_con_username(self):
        """Test autenticación con username"""
        from django.contrib.auth import authenticate
        user = authenticate(username='test_user', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'test_user')
    
    def test_autenticacion_con_rut(self):
        """Test autenticación con RUT usando backend personalizado"""
        from apps.administracion.backends import RUTAuthenticationBackend
        backend = RUTAuthenticationBackend()
        user = backend.authenticate(None, username='12.345.678-5', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user.rut, '12.345.678-5')
    
    def test_autenticacion_credenciales_incorrectas(self):
        """Test autenticación con credenciales incorrectas"""
        from django.contrib.auth import authenticate
        user = authenticate(username='test_user', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_bloqueo_manual_cuenta(self):
        """Test que el bloqueo manual de cuenta funciona"""
        self.assertTrue(self.usuario.activo)  # Usar campo activo personalizado
        self.assertFalse(self.usuario.cuenta_bloqueada)
        
        # Bloquear cuenta
        self.usuario.bloquear_cuenta()
        
        # Verificar estado
        self.assertFalse(self.usuario.activo)  # Usar campo activo personalizado
        self.assertTrue(self.usuario.cuenta_bloqueada)


class LogoutViewTest(TestCase):
    """Tests para la vista de logout"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            rut='12.345.678-5',
            password='testpass123',
            rol='matrona'
        )
        self.client.login(username='test_user', password='testpass123')
    
    def test_logout_exitoso(self):
        """Test logout exitoso"""
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class AuditoriaModelTest(TestCase):
    """Tests para el modelo de Auditoría"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create_user(
            username='test_user',
            rut='12.345.678-5',
            password='testpass123',
            rol='matrona'
        )
    
    def test_crear_registro_auditoria(self):
        """Test creación de registro de auditoría"""
        auditoria = Auditoria.objects.create(
            usuario=self.usuario,
            accion='CREATE',
            modelo='PacienteMadre',
            objeto_id=1,
            descripcion='Creó paciente',
            ip_address='127.0.0.1'
        )
        self.assertEqual(auditoria.usuario, self.usuario)
        self.assertEqual(auditoria.accion, 'CREATE')
        self.assertIsNotNone(auditoria.timestamp)
    
    def test_auditoria_inmutable(self):
        """Test que los registros de auditoría no se pueden editar"""
        auditoria = Auditoria.objects.create(
            usuario=self.usuario,
            accion='CREATE',
            modelo='PacienteMadre',
            objeto_id=1,
            descripcion='Creó paciente',
            ip_address='127.0.0.1'
        )
        
        # Intentar modificar
        auditoria.descripcion = 'Modificado'
        
        # El save debería prevenir la modificación
        with self.assertRaises(Exception):
            auditoria.save()
    
    def test_auditoria_no_eliminable(self):
        """Test que los registros de auditoría no se pueden eliminar"""
        auditoria = Auditoria.objects.create(
            usuario=self.usuario,
            accion='CREATE',
            modelo='PacienteMadre',
            objeto_id=1,
            descripcion='Creó paciente',
            ip_address='127.0.0.1'
        )
        
        # Intentar eliminar
        with self.assertRaises(Exception):
            auditoria.delete()
    
    def test_auditoria_ordenamiento(self):
        """Test que los registros se ordenan por timestamp descendente"""
        # Crear varios registros
        for i in range(3):
            Auditoria.objects.create(
                usuario=self.usuario,
                accion='CREATE',
                modelo='Test',
                objeto_id=i,
                descripcion=f'Acción {i}',
                ip_address='127.0.0.1'
            )
        
        registros = Auditoria.objects.all()
        # El más reciente debería ser el primero
        self.assertEqual(registros[0].objeto_id, 2)
        self.assertEqual(registros[2].objeto_id, 0)


class PermisosRolTest(TestCase):
    """Tests de permisos según rol de usuario"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = Client()
    
    def test_matrona_puede_acceder_registro_parto(self):
        """Test que matrona puede acceder a registro de parto"""
        usuario = Usuario.objects.create_user(
            username='matrona',
            rut='12.345.678-5',
            password='test123',
            rol='matrona'
        )
        self.client.login(username='matrona', password='test123')
        
        # Verificar permisos
        self.assertTrue(usuario.puede_registrar_parto())
    
    def test_pediatra_puede_acceder_evaluacion_rn(self):
        """Test que pediatra puede acceder a evaluación de RN"""
        usuario = Usuario.objects.create_user(
            username='pediatra',
            rut='11.111.111-1',
            password='test123',
            rol='pediatra'
        )
        self.client.login(username='pediatra', password='test123')
        
        # Verificar permisos
        self.assertTrue(usuario.puede_evaluar_rn())
        self.assertFalse(usuario.puede_registrar_parto())
    
    def test_jefe_servicio_puede_generar_reportes(self):
        """Test que jefe de servicio puede generar reportes"""
        usuario = Usuario.objects.create_user(
            username='jefe',
            rut='22.222.222-2',
            password='test123',
            rol='jefe_servicio'
        )
        
        self.assertTrue(usuario.puede_generar_reportes())
        self.assertTrue(usuario.puede_ver_datos_sensibles())
    
    def test_super_admin_puede_gestionar_usuarios(self):
        """Test que super admin puede gestionar usuarios"""
        usuario = Usuario.objects.create_user(
            username='admin',
            rut='33.333.333-3',
            password='test123',
            rol='super_admin'
        )
        
        self.assertTrue(usuario.puede_gestionar_usuarios())
        self.assertTrue(usuario.puede_generar_reportes())
