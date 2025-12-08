from django.test import TestCase
from django.utils import timezone
from apps.pacientes.models import PacienteMadre
from apps.obstetricia.models import Parto
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class RobsonClassificationTest(TestCase):
    def setUp(self):
        # Crear usuario para registro
        self.usuario = Usuario.objects.create(
            username='matrona_test',
            rut='12.345.678-9',
            rol='matrona'
        )
        
        # Crear paciente base
        self.paciente = PacienteMadre.objects.create(
            rut='11.111.111-1',
            nombre='Ana',
            apellido_paterno='Test',
            apellido_materno='Prueba',
            fecha_nacimiento='1990-01-01',
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle Falsa 123',
            comuna='Chillán',
            region='Ñuble'
        )

    def create_parto(self, **kwargs):
        defaults = {
            'paciente': self.paciente,
            'usuario_registro': self.usuario,
            'fecha_parto': timezone.now().date(),
            'hora_parto': timezone.now().time(),
            'edad_gestacional_semanas': 39,
            'edad_gestacional_dias': 0,
            'tipo_parto': 'eutocico',
            'presentacion': 'cefalica',
            'inicio_trabajo_parto': 'espontaneo',
            'primigesta': True,
            'multigesta': False,
            'cicatriz_uterina': False,
            'grupo_robson': 0 # Se recalculará al guardar
        }
        defaults.update(kwargs)
        return Parto.objects.create(**defaults)

    def test_robson_grupo_1(self):
        """
        Grupo 1: Nulíparas, único, cefálico, >=37 sem, espontáneo
        """
        parto = self.create_parto(
            primigesta=True,
            multigesta=False,
            presentacion='cefalica',
            edad_gestacional_semanas=39,
            inicio_trabajo_parto='espontaneo'
        )
        self.assertEqual(parto.grupo_robson, 1)

    def test_robson_grupo_2(self):
        """
        Grupo 2: Nulíparas, único, cefálico, >=37 sem, inducido o cesárea antes t.p.
        """
        parto = self.create_parto(
            primigesta=True,
            multigesta=False,
            presentacion='cefalica',
            edad_gestacional_semanas=39,
            inicio_trabajo_parto='inducido'
        )
        self.assertEqual(parto.grupo_robson, 2)

    def test_robson_grupo_3(self):
        """
        Grupo 3: Multíparas sin cicatriz, único, cefálico, >=37 sem, espontáneo
        """
        parto = self.create_parto(
            primigesta=False,
            multigesta=True,
            cicatriz_uterina=False,
            presentacion='cefalica',
            edad_gestacional_semanas=39,
            inicio_trabajo_parto='espontaneo'
        )
        self.assertEqual(parto.grupo_robson, 3)

    def test_robson_grupo_5(self):
        """
        Grupo 5: Multíparas con cicatriz previa, único, cefálico, >=37 sem
        """
        parto = self.create_parto(
            primigesta=False,
            multigesta=True,
            cicatriz_uterina=True,
            presentacion='cefalica',
            edad_gestacional_semanas=39
        )
        self.assertEqual(parto.grupo_robson, 5)

    def test_robson_grupo_6(self):
        """
        Grupo 6: Nulíparas, podálica
        """
        parto = self.create_parto(
            primigesta=True,
            multigesta=False,
            presentacion='podalica',
            edad_gestacional_semanas=39
        )
        self.assertEqual(parto.grupo_robson, 6)

    def test_robson_grupo_10(self):
        """
        Grupo 10: Prematuros (<37 semanas), único, cefálico
        """
        parto = self.create_parto(
            primigesta=True,
            presentacion='cefalica',
            edad_gestacional_semanas=36 # Prematuro
        )
        self.assertEqual(parto.grupo_robson, 10)

    def test_robson_grupo_4(self):
        """
        Grupo 4: Multíparas sin cicatriz, único, cefálico, ≥37 sem, inducido o cesárea antes t.p.
        """
        parto = self.create_parto(
            primigesta=False,
            multigesta=True,
            cicatriz_uterina=False,
            presentacion='cefalica',
            edad_gestacional_semanas=39,
            inicio_trabajo_parto='inducido'
        )
        self.assertEqual(parto.grupo_robson, 4)

    def test_robson_grupo_7(self):
        """
        Grupo 7: Multíparas, podálica (incluye cicatriz)
        """
        parto = self.create_parto(
            primigesta=False,
            multigesta=True,
            presentacion='podalica',
            edad_gestacional_semanas=39
        )
        self.assertEqual(parto.grupo_robson, 7)

    def test_robson_grupo_8(self):
        """
        Grupo 8: Embarazos múltiples
        Nota: Requiere ControlPrenatal con embarazo_gemelar=True
        """
        # Crear control prenatal con embarazo gemelar
        from apps.obstetricia.models import ControlPrenatal
        from datetime import date
        
        control = ControlPrenatal.objects.create(
            paciente=self.paciente,
            fur=date(2024, 1, 1),
            embarazo_gemelar=True
        )
        
        parto = Parto.objects.create(
            paciente=self.paciente,
            usuario_registro=self.usuario,
            control_prenatal=control,
            fecha_parto=timezone.now().date(),
            hora_parto=timezone.now().time(),
            edad_gestacional_semanas=37,
            edad_gestacional_dias=0,
            tipo_parto='eutocico',
            presentacion='cefalica',
            inicio_trabajo_parto='espontaneo',
            primigesta=True,
            multigesta=False,
            cicatriz_uterina=False,
            grupo_robson=0
        )
        self.assertEqual(parto.grupo_robson, 8)

    def test_robson_grupo_9(self):
        """
        Grupo 9: Presentación transversa/oblicua
        """
        parto = self.create_parto(
            primigesta=True,
            presentacion='transversa',
            edad_gestacional_semanas=39
        )
        self.assertEqual(parto.grupo_robson, 9)

    def test_recalculo_robson_al_guardar(self):
        """Test que el grupo Robson se recalcula automáticamente al guardar"""
        parto = self.create_parto(
            primigesta=True,
            presentacion='cefalica',
            edad_gestacional_semanas=39,
            inicio_trabajo_parto='espontaneo'
        )
        self.assertEqual(parto.grupo_robson, 1)
        
        # Cambiar a inducido
        parto.inicio_trabajo_parto = 'inducido'
        parto.save()
        
        # Debería cambiar a grupo 2
        self.assertEqual(parto.grupo_robson, 2)


class ProtocoloVIHTest(TestCase):
    """Tests para el protocolo VIH automático"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create(
            username='matrona_test',
            rut='12.345.678-9',
            rol='matrona'
        )
        
        self.paciente = PacienteMadre.objects.create(
            rut='11.111.111-1',
            nombre='Ana',
            apellido_paterno='Test',
            apellido_materno='Prueba',
            fecha_nacimiento='1990-01-01',
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle Falsa 123',
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
    
    def test_crear_protocolo_vih(self):
        """Test creación de protocolo VIH para un parto"""
        from apps.obstetricia.models import ProtocoloVIH
        
        protocolo = ProtocoloVIH.objects.create(
            parto=self.parto,
            activado=True
        )
        
        self.assertTrue(protocolo.activado)
        self.assertEqual(protocolo.parto, self.parto)
    
    def test_activar_protocolo_vih(self):
        """Test activación automática del protocolo VIH"""
        from apps.obstetricia.models import ProtocoloVIH
        
        protocolo = ProtocoloVIH.objects.create(
            parto=self.parto,
            activado=False
        )
        
        # Activar protocolo
        protocolo.activar_protocolo()
        
        self.assertTrue(protocolo.activado)
        self.assertIsNotNone(protocolo.fecha_activacion)
        self.assertTrue(protocolo.cesarea_electiva_recomendada)
        self.assertTrue(protocolo.lactancia_suspendida)


class ValidacionCamposPartoTest(TestCase):
    """Tests de validación de campos del modelo Parto"""
    
    def setUp(self):
        """Configuración inicial"""
        self.usuario = Usuario.objects.create(
            username='matrona_test',
            rut='12.345.678-9',
            rol='matrona'
        )
        
        self.paciente = PacienteMadre.objects.create(
            rut='11.111.111-1',
            nombre='Ana',
            apellido_paterno='Test',
            apellido_materno='Prueba',
            fecha_nacimiento='1990-01-01',
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle Falsa 123',
            comuna='Chillán',
            region='Ñuble'
        )
    
    def test_edad_gestacional_valida(self):
        """Test que acepta edad gestacional válida (20-43 semanas)"""
        parto = Parto.objects.create(
            paciente=self.paciente,
            usuario_registro=self.usuario,
            fecha_parto=timezone.now().date(),
            hora_parto=timezone.now().time(),
            edad_gestacional_semanas=40,
            edad_gestacional_dias=0,
            tipo_parto='eutocico',
            presentacion='cefalica',
            inicio_trabajo_parto='espontaneo',
            grupo_robson=1
        )
        self.assertEqual(parto.edad_gestacional_semanas, 40)
    
    def test_relacion_con_paciente(self):
        """Test que el parto está correctamente relacionado con la paciente"""
        parto = Parto.objects.create(
            paciente=self.paciente,
            usuario_registro=self.usuario,
            fecha_parto=timezone.now().date(),
            hora_parto=timezone.now().time(),
            edad_gestacional_semanas=39,
            tipo_parto='eutocico',
            presentacion='cefalica',
            inicio_trabajo_parto='espontaneo',
            grupo_robson=1
        )
        
        self.assertEqual(parto.paciente, self.paciente)
        self.assertIn(parto, self.paciente.partos.all())
