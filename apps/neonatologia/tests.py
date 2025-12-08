from django.test import TestCase
from django.utils import timezone
from apps.pacientes.models import PacienteMadre
from apps.obstetricia.models import Parto
from apps.neonatologia.models import RecienNacido
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class ApgarAlertTest(TestCase):
    def setUp(self):
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
            grupo_robson=1
        )

    def test_apgar_normal(self):
        """Test RN con APGAR normal no genera alerta crítica"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=3200,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=9, # Normal >= 7
            destino='alojamiento_conjunto'
        )
        self.assertFalse(rn.apgar_5_critico)
        self.assertFalse(rn.requiere_alerta_pediatra)

    def test_apgar_critico(self):
        """Test RN con APGAR < 7 genera alerta crítica"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='masculino',
            peso_gramos=3000,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=5,
            apgar_5_min=6, # Crítico < 7
            destino='neonatologia'
        )
        self.assertTrue(rn.apgar_5_critico)
        self.assertTrue(rn.requiere_alerta_pediatra)

    def test_bajo_peso_alerta(self):
        """Test RN con bajo peso genera alerta aunque APGAR sea normal"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=2400, # Bajo peso < 2500
            talla_cm=48.0,
            circunferencia_craneana_cm=33.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto'
        )
        self.assertFalse(rn.apgar_5_critico)
        self.assertTrue(rn.requiere_alerta_pediatra)
        self.assertEqual(rn.clasificacion_peso, 'Bajo Peso (1500-2499g)')

    def test_macrosomico_alerta(self):
        """Test RN macrosómico (>4000g) genera alerta"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='masculino',
            peso_gramos=4200,  # Macrosómico > 4000g
            talla_cm=53.0,
            circunferencia_craneana_cm=36.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto'
        )
        self.assertTrue(rn.requiere_alerta_pediatra)
        self.assertEqual(rn.clasificacion_peso, 'Macrosómico (>4000g)')

    def test_apgar_valores_directos(self):
        """Test que los valores APGAR se almacenan correctamente"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=3200,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=10,
            destino='alojamiento_conjunto'
        )
        
        # Verificar que los valores se guardaron correctamente
        self.assertEqual(rn.apgar_1_min, 8)
        self.assertEqual(rn.apgar_5_min, 10)
        self.assertFalse(rn.apgar_5_critico)

    def test_clasificacion_peso_normal(self):
        """Test clasificación de peso normal (2500-4000g)"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=3200,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto'
        )
        self.assertEqual(rn.clasificacion_peso, 'Normal (2500-4000g)')

    def test_clasificacion_muy_bajo_peso(self):
        """Test clasificación de muy bajo peso (<1500g)"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='masculino',
            peso_gramos=1200,
            talla_cm=42.0,
            circunferencia_craneana_cm=30.0,
            apgar_1_min=6,
            apgar_5_min=7,
            destino='neonatologia'
        )
        self.assertEqual(rn.clasificacion_peso, 'Muy Bajo Peso (<1500g)')
        self.assertTrue(rn.requiere_alerta_pediatra)

    def test_relacion_con_parto(self):
        """Test que el RN está correctamente relacionado con el parto"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=3200,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto'
        )
        
        self.assertEqual(rn.parto, self.parto)
        # Verificar que se puede acceder al RN desde el parto
        self.assertTrue(hasattr(self.parto, 'recien_nacido'))

    def test_edad_gestacional_capurro(self):
        """Test que acepta edad gestacional por Capurro"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='masculino',
            peso_gramos=3000,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto',
            edad_gestacional_capurro=39
        )
        
        self.assertEqual(rn.edad_gestacional_capurro, 39)

    def test_procedimientos_inmediatos(self):
        """Test registro de procedimientos inmediatos"""
        rn = RecienNacido.objects.create(
            parto=self.parto,
            sexo='femenino',
            peso_gramos=3200,
            talla_cm=50.0,
            circunferencia_craneana_cm=35.0,
            apgar_1_min=8,
            apgar_5_min=9,
            destino='alojamiento_conjunto',
            apego_piel_a_piel=True,
            lactancia_inmediata=True,
            vitamina_k_administrada=True,
            profilaxis_ocular=True
        )
        
        self.assertTrue(rn.apego_piel_a_piel)
        self.assertTrue(rn.lactancia_inmediata)
        self.assertTrue(rn.vitamina_k_administrada)
        self.assertTrue(rn.profilaxis_ocular)
