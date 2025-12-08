from django.test import TestCase
from django.utils import timezone
from datetime import date
from apps.administracion.models import Usuario
from apps.pacientes.models import PacienteMadre
from apps.obstetricia.models import Parto


class PermisosReportesTest(TestCase):
    """Tests para permisos de generación de reportes"""
    
    def test_jefe_servicio_puede_generar_reportes(self):
        """Test que jefe de servicio puede generar reportes"""
        usuario = Usuario.objects.create_user(
            username='jefe',
            rut='11.111.111-1',
            password='test123',
            rol='jefe_servicio'
        )
        self.assertTrue(usuario.puede_generar_reportes())
    
    def test_super_admin_puede_generar_reportes(self):
        """Test que super admin puede generar reportes"""
        usuario = Usuario.objects.create_user(
            username='admin',
            rut='12.345.678-5',
            password='test123',
            rol='super_admin'
        )
        self.assertTrue(usuario.puede_generar_reportes())
    
    def test_administrativo_puede_generar_reportes(self):
        """Test que administrativo puede generar reportes"""
        usuario = Usuario.objects.create_user(
            username='admin_user',
            rut='98.765.432-1',
            password='test123',
            rol='administrativo'
        )
        self.assertTrue(usuario.puede_generar_reportes())
    
    def test_matrona_no_puede_generar_reportes(self):
        """Test que matrona NO puede generar reportes"""
        usuario = Usuario.objects.create_user(
            username='matrona',
            rut='11.222.333-4',
            password='test123',
            rol='matrona'
        )
        self.assertFalse(usuario.puede_generar_reportes())


class ReportesEstadisticosTest(TestCase):
    """Tests para reportes estadísticos"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create_user(
            username='jefe_test',
            rut='12.345.678-5',
            password='testpass123',
            rol='jefe_servicio'
        )
        
        # Crear múltiples pacientes y partos para estadísticas
        for i in range(5):
            paciente = PacienteMadre.objects.create(
                rut=f'1{i}.111.111-{i}',
                nombre=f'Paciente{i}',
                apellido_paterno='Test',
                apellido_materno='Prueba',
                fecha_nacimiento=date(1990, 1, 1),
                estado_civil='soltera',
                escolaridad='media_completa',
                prevision='fonasa_b',
                direccion='Calle Test',
                comuna='Chillán',
                region='Ñuble'
            )
            
            Parto.objects.create(
                paciente=paciente,
                usuario_registro=self.usuario,
                fecha_parto=timezone.now().date(),
                hora_parto=timezone.now().time(),
                edad_gestacional_semanas=39,
                edad_gestacional_dias=0,
                tipo_parto='eutocico' if i % 2 == 0 else 'cesarea_electiva',
                presentacion='cefalica',
                inicio_trabajo_parto='espontaneo',
                primigesta=True if i % 2 == 0 else False,
                multigesta=False if i % 2 == 0 else True,
                grupo_robson=1 if i % 2 == 0 else 2
            )
    
    def test_conteo_partos(self):
        """Test que el conteo de partos es correcto"""
        total_partos = Parto.objects.count()
        self.assertEqual(total_partos, 5)
    
    def test_distribucion_tipo_parto(self):
        """Test distribución de tipos de parto"""
        eutocicos = Parto.objects.filter(tipo_parto='eutocico').count()
        cesareas = Parto.objects.filter(tipo_parto='cesarea_electiva').count()
        
        self.assertEqual(eutocicos, 3)  # 0, 2, 4
        self.assertEqual(cesareas, 2)   # 1, 3
    
    def test_distribucion_grupos_robson(self):
        """Test distribución de grupos Robson"""
        grupo_1 = Parto.objects.filter(grupo_robson=1).count()
        grupo_2 = Parto.objects.filter(grupo_robson=2).count()
        
        self.assertEqual(grupo_1, 3)
        self.assertEqual(grupo_2, 2)


class ValidacionDatosReporteTest(TestCase):
    """Tests de validación de datos en reportes"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create_user(
            username='jefe_test',
            rut='12.345.678-5',
            password='testpass123',
            rol='jefe_servicio'
        )
        
        self.paciente = PacienteMadre.objects.create(
            rut='11.111.111-1',
            nombre='Ana',
            apellido_paterno='González',
            apellido_materno='Silva',
            fecha_nacimiento=date(1990, 5, 15),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle Principal 123',
            comuna='Chillán',
            region='Ñuble'
        )
        
        self.parto = Parto.objects.create(
            paciente=self.paciente,
            usuario_registro=self.usuario,
            fecha_parto=timezone.now().date(),
            hora_parto=timezone.now().time(),
            edad_gestacional_semanas=39,
            edad_gestacional_dias=0,
            tipo_parto='eutocico',
            presentacion='cefalica',
            inicio_trabajo_parto='espontaneo',
            primigesta=True,
            multigesta=False,
            grupo_robson=1
        )
    
    def test_parto_tiene_paciente_asociado(self):
        """Test que el parto tiene paciente asociado para el reporte"""
        self.assertIsNotNone(self.parto.paciente)
        self.assertEqual(self.parto.paciente, self.paciente)
    
    def test_parto_tiene_fecha_valida(self):
        """Test que el parto tiene fecha válida"""
        self.assertIsNotNone(self.parto.fecha_parto)
        self.assertIsInstance(self.parto.fecha_parto, date)
    
    def test_parto_tiene_grupo_robson(self):
        """Test que el parto tiene grupo Robson calculado"""
        self.assertIsNotNone(self.parto.grupo_robson)
        self.assertGreaterEqual(self.parto.grupo_robson, 1)
        self.assertLessEqual(self.parto.grupo_robson, 10)
