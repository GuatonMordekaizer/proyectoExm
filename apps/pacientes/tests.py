from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from apps.pacientes.models import PacienteMadre, validar_rut


class ValidarRUTTest(TestCase):
    """Tests para la validación de RUT chileno"""
    
    def test_rut_valido_con_digito_numerico(self):
        """Test RUT válido con dígito verificador numérico"""
        try:
            validar_rut('12.345.678-5')
        except ValidationError:
            self.fail('RUT válido fue rechazado')
    
    def test_rut_valido_con_k(self):
        """Test RUT válido con dígito verificador K"""
        # 11.111.112-K es un RUT válido con K (verificado)
        try:
            validar_rut('11.111.112-K')
        except ValidationError:
            self.fail('RUT válido con K fue rechazado')
    
    def test_rut_digito_verificador_incorrecto(self):
        """Test RUT con dígito verificador incorrecto"""
        with self.assertRaises(ValidationError):
            validar_rut('12.345.678-9')  # DV correcto es 5
    
    def test_rut_formato_sin_puntos(self):
        """Test RUT válido sin puntos"""
        try:
            validar_rut('12345678-5')
        except ValidationError:
            self.fail('RUT válido sin puntos fue rechazado')
    
    def test_rut_muy_corto(self):
        """Test RUT muy corto"""
        with self.assertRaises(ValidationError):
            validar_rut('1-2')


class PacienteMadreModelTest(TestCase):
    """Tests para el modelo PacienteMadre"""
    
    def test_crear_paciente_valido(self):
        """Test creación de paciente con datos válidos"""
        paciente = PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='María',
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
        self.assertEqual(paciente.rut, '12.345.678-5')
        self.assertEqual(paciente.nombre, 'María')
    
    def test_rut_unico(self):
        """Test que el RUT debe ser único"""
        PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Paciente1',
            apellido_paterno='Apellido1',
            apellido_materno='Apellido2',
            fecha_nacimiento=date(1990, 1, 1),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle 1',
            comuna='Chillán',
            region='Ñuble'
        )
        
        # Intentar crear otro paciente con el mismo RUT
        with self.assertRaises(Exception):
            PacienteMadre.objects.create(
                rut='12.345.678-5',
                nombre='Paciente2',
                apellido_paterno='Otro',
                apellido_materno='Apellido',
                fecha_nacimiento=date(1995, 5, 5),
                estado_civil='casada',
                escolaridad='universitaria_completa',
                prevision='fonasa_a',
                direccion='Calle 2',
                comuna='Chillán',
                region='Ñuble'
            )
    
    def test_nombre_completo_property(self):
        """Test propiedad nombre_completo"""
        paciente = PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Ana',
            apellido_paterno='Pérez',
            apellido_materno='López',
            fecha_nacimiento=date(1990, 1, 1),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle 1',
            comuna='Chillán',
            region='Ñuble'
        )
        self.assertEqual(paciente.nombre_completo, 'Ana Pérez López')
    
    def test_edad_property(self):
        """Test propiedad edad"""
        paciente = PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Laura',
            apellido_paterno='Martínez',
            apellido_materno='Rojas',
            fecha_nacimiento=date(1990, 1, 1),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle 1',
            comuna='Chillán',
            region='Ñuble'
        )
        # La edad debería ser aproximadamente 34-35 años (2024/2025)
        self.assertGreaterEqual(paciente.edad, 30)
        self.assertLessEqual(paciente.edad, 40)
    
    def test_str_method(self):
        """Test método __str__"""
        paciente = PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Carmen',
            apellido_paterno='Soto',
            apellido_materno='Vega',
            fecha_nacimiento=date(1992, 3, 20),
            estado_civil='casada',
            escolaridad='universitaria_completa',
            prevision='fonasa_c',
            direccion='Av. Principal 456',
            comuna='Chillán',
            region='Ñuble'
        )
        expected = 'Carmen Soto (12.345.678-5)'
        self.assertEqual(str(paciente), expected)


class BusquedaPacienteTest(TestCase):
    """Tests para la funcionalidad de búsqueda de pacientes"""
    
    def setUp(self):
        """Configuración inicial"""
        # Crear pacientes de prueba
        PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Ana',
            apellido_paterno='Pérez',
            apellido_materno='López',
            fecha_nacimiento=date(1990, 1, 1),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle 1',
            comuna='Chillán',
            region='Ñuble'
        )
        
        PacienteMadre.objects.create(
            rut='98.765.432-1',
            nombre='María',
            apellido_paterno='González',
            apellido_materno='Silva',
            fecha_nacimiento=date(1985, 5, 15),
            estado_civil='casada',
            escolaridad='universitaria_completa',
            prevision='fonasa_a',
            direccion='Calle 2',
            comuna='Chillán',
            region='Ñuble'
        )
    
    def test_busqueda_por_rut(self):
        """Test búsqueda de paciente por RUT"""
        from django.db.models import Q
        pacientes = PacienteMadre.objects.filter(
            Q(rut__icontains='12.345.678')
        )
        self.assertEqual(pacientes.count(), 1)
        self.assertEqual(pacientes.first().nombre, 'Ana')
    
    def test_busqueda_por_nombre(self):
        """Test búsqueda de paciente por nombre"""
        from django.db.models import Q
        pacientes = PacienteMadre.objects.filter(
            Q(nombre__icontains='María')
        )
        self.assertEqual(pacientes.count(), 1)
        self.assertEqual(pacientes.first().apellido_paterno, 'González')
    
    def test_busqueda_por_apellido(self):
        """Test búsqueda de paciente por apellido"""
        from django.db.models import Q
        pacientes = PacienteMadre.objects.filter(
            Q(apellido_paterno__icontains='Pérez')
        )
        self.assertEqual(pacientes.count(), 1)
        self.assertEqual(pacientes.first().nombre, 'Ana')
    
    def test_busqueda_sin_resultados(self):
        """Test búsqueda sin resultados"""
        from django.db.models import Q
        pacientes = PacienteMadre.objects.filter(
            Q(nombre__icontains='NoExiste')
        )
        self.assertEqual(pacientes.count(), 0)


class CrearPacienteTest(TestCase):
    """Tests para la funcionalidad de creación de pacientes"""
    
    def test_crear_paciente_con_datos_validos(self):
        """Test creación de paciente con datos válidos"""
        paciente = PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Carla',
            apellido_paterno='Rojas',
            apellido_materno='Muñoz',
            fecha_nacimiento=date(1992, 3, 20),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Av. Principal 456',
            comuna='Chillán',
            region='Ñuble'
        )
        
        # Verificar que se creó correctamente
        self.assertTrue(PacienteMadre.objects.filter(rut='12.345.678-5').exists())
        self.assertEqual(paciente.nombre, 'Carla')
        self.assertEqual(paciente.apellido_paterno, 'Rojas')
    
    def test_crear_paciente_rut_duplicado(self):
        """Test que no se puede crear paciente con RUT duplicado"""
        # Crear primer paciente
        PacienteMadre.objects.create(
            rut='12.345.678-5',
            nombre='Paciente1',
            apellido_paterno='Apellido1',
            apellido_materno='Apellido2',
            fecha_nacimiento=date(1990, 1, 1),
            estado_civil='soltera',
            escolaridad='media_completa',
            prevision='fonasa_b',
            direccion='Calle 1',
            comuna='Chillán',
            region='Ñuble'
        )
        
        # Intentar crear segundo paciente con mismo RUT
        with self.assertRaises(Exception):
            PacienteMadre.objects.create(
                rut='12.345.678-5',
                nombre='Paciente2',
                apellido_paterno='Otro',
                apellido_materno='Apellido',
                fecha_nacimiento=date(1995, 5, 5),
                estado_civil='casada',
                escolaridad='universitaria_completa',
                prevision='fonasa_a',
                direccion='Calle 2',
                comuna='Chillán',
                region='Ñuble'
            )
