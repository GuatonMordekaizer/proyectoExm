"""
Test de Selenium para automatizar la creación de pacientes.
Prueba el formulario completo de registro de paciente madre.
"""

import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def generar_rut_valido():
    """Genera un RUT chileno válido aleatorio"""
    import random
    
    # Generar número aleatorio entre 5.000.000 y 25.000.000
    numero = random.randint(5000000, 25000000)
    
    # Calcular dígito verificador
    suma = 0
    multiplo = 2
    
    for digito in reversed(str(numero)):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        dv = '0'
    elif dv_calculado == 10:
        dv = 'K'
    else:
        dv = str(dv_calculado)
    
    # Formatear con puntos y guión
    rut_str = str(numero)
    rut_formateado = f"{rut_str[:-6]}.{rut_str[-6:-3]}.{rut_str[-3:]}-{dv}"
    
    return rut_formateado


def test_crear_paciente():
    """
    Test completo de creación de paciente madre.
    Completa todos los campos del formulario y verifica el registro exitoso.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("=" * 80)
        print("TEST: CREAR PACIENTE MADRE")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN
        # ===================================================================
        print("\n[1/3] Iniciando sesión...")
        driver.get("http://127.0.0.1:8000/auth/login/")
        
        # Login como usuario médico
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("medico_g")
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("doc@12345678")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Esperar que cargue el dashboard
        time.sleep(2)
        print("✓ Sesión iniciada como medico_g")
        
        # ===================================================================
        # PASO 2: NAVEGAR AL FORMULARIO DE CREAR PACIENTE
        # ===================================================================
        print("\n[2/3] Navegando al formulario de crear paciente...")
        driver.get("http://127.0.0.1:8000/pacientes/crear/")
        
        # Esperar que cargue el formulario
        wait.until(EC.presence_of_element_located((By.NAME, "rut")))
        print("✓ Formulario de crear paciente cargado")
        
        # ===================================================================
        # PASO 3: COMPLETAR FORMULARIO
        # ===================================================================
        print("\n[3/3] Completando formulario de paciente...")
        
        # Generar datos de prueba
        rut_paciente = generar_rut_valido()
        # Edad válida: entre 10 y 60 años (generamos 25 años)
        import random
        edad_anios = random.randint(18, 45)  # Edad típica para embarazos
        fecha_nacimiento = (date.today() - timedelta(days=365*edad_anios + random.randint(0, 364))).strftime('%Y-%m-%d')
        
        print(f"\nDatos del paciente a crear:")
        print(f"  RUT: {rut_paciente}")
        print(f"  Nombre: María Isabel")
        print(f"  Apellidos: González Pérez")
        print(f"  Fecha Nacimiento: {fecha_nacimiento} ({edad_anios} años)")
        print(f"  Estado Civil: Casada")
        print(f"  Escolaridad: Media Completa")
        print(f"  Previsión: FONASA B")
        print(f"  Comuna: Chillán")
        print(f"  Región: Ñuble")
        
        # --- SECCIÓN: IDENTIFICACIÓN ---
        print("\n  Completando identificación...")
        
        rut_input = driver.find_element(By.ID, "id_rut")
        rut_input.clear()
        rut_input.send_keys(rut_paciente)
        
        nombre_input = driver.find_element(By.ID, "id_nombre")
        nombre_input.clear()
        nombre_input.send_keys("María Isabel")
        
        apellido_paterno_input = driver.find_element(By.ID, "id_apellido_paterno")
        apellido_paterno_input.clear()
        apellido_paterno_input.send_keys("González")
        
        apellido_materno_input = driver.find_element(By.ID, "id_apellido_materno")
        apellido_materno_input.clear()
        apellido_materno_input.send_keys("Pérez")
        
        print("    ✓ Datos de identificación completados")
        
        # --- SECCIÓN: DATOS DEMOGRÁFICOS ---
        print("\n  Completando datos demográficos...")
        
        fecha_nacimiento_input = driver.find_element(By.ID, "id_fecha_nacimiento")
        # Para campos type="date", usar setAttribute es más confiable que send_keys
        driver.execute_script(f"arguments[0].value = '{fecha_nacimiento}';", fecha_nacimiento_input)
        
        estado_civil_select = Select(driver.find_element(By.ID, "id_estado_civil"))
        estado_civil_select.select_by_value("casada")
        
        escolaridad_select = Select(driver.find_element(By.ID, "id_escolaridad"))
        escolaridad_select.select_by_value("media_completa")
        
        prevision_select = Select(driver.find_element(By.ID, "id_prevision"))
        prevision_select.select_by_value("fonasa_B")
        
        telefono_input = driver.find_element(By.ID, "id_telefono")
        telefono_input.clear()
        telefono_input.send_keys("+56942123456")
        
        # Checkbox pueblo originario (dejar desmarcado)
        pueblo_originario_checkbox = driver.find_element(By.ID, "id_pueblo_originario")
        if pueblo_originario_checkbox.is_selected():
            pueblo_originario_checkbox.click()
        
        print("    ✓ Datos demográficos completados")
        
        # --- SECCIÓN: UBICACIÓN ---
        print("\n  Completando ubicación...")
        
        direccion_input = driver.find_element(By.ID, "id_direccion")
        direccion_input.clear()
        direccion_input.send_keys("Avenida Argentina 123, Población Villa Los Aromos")
        
        comuna_input = driver.find_element(By.ID, "id_comuna")
        comuna_input.clear()
        comuna_input.send_keys("Chillán")
        
        region_input = driver.find_element(By.ID, "id_region")
        region_input.clear()
        region_input.send_keys("Ñuble")
        
        print("    ✓ Ubicación completada")
        
        # Campo consultorio_origen ahora está en el template
        try:
            consultorio_input = driver.find_element(By.ID, "id_consultorio_origen")
            consultorio_input.clear()
            consultorio_input.send_keys("CESFAM Dr. Víctor Manuel Fernández")
            print("    ✓ Consultorio de origen completado")
        except NoSuchElementException:
            print("    ⚠ Campo consultorio_origen no encontrado")
        
        # ===================================================================
        # PASO 4: ENVIAR FORMULARIO
        # ===================================================================
        print("\n[4/4] Enviando formulario...")
        time.sleep(1)  # Pausa para verificar datos antes de enviar
        
        # Verificar que seguimos autenticados
        current_url_before = driver.current_url
        print(f"  URL antes de enviar: {current_url_before}")
        
        if "/auth/login/" in current_url_before:
            print("✗ ERROR: La sesión se perdió antes de enviar el formulario")
            raise Exception("Sesión perdida antes de enviar")
        
        # Buscar el botón correcto (hay 2 submit buttons, necesitamos el primario)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        
        # Verificar que estamos autenticados antes de enviar
        try:
            driver.find_element(By.NAME, "rut")  # Si encontramos el campo, estamos en el form
            print("✓ Formulario listo para enviar")
        except NoSuchElementException:
            print("✗ ERROR: Perdimos la sesión o el formulario")
            raise
        
        # Guardar el RUT para verificación posterior
        rut_creado = rut_paciente
        
        # Verificar que el token CSRF esté presente
        try:
            csrf_input = driver.find_element(By.CSS_SELECTOR, "input[name='csrfmiddlewaretoken']")
            csrf_value = csrf_input.get_attribute('value')
            if csrf_value:
                print(f"✓ Token CSRF presente: {csrf_value[:20]}...")
            else:
                print("⚠ Token CSRF vacío")
        except NoSuchElementException:
            print("✗ ERROR: No se encontró token CSRF")
            raise
        
        # Enviar formulario usando JavaScript (más confiable que click directo)
        driver.execute_script("arguments[0].click();", submit_button)
        print("✓ Formulario enviado")
        
        # ===================================================================
        # PASO 5: VERIFICAR RESULTADO
        # ===================================================================
        print("\n[5/5] Verificando resultado...")
        time.sleep(3)  # Esperar procesamiento del formulario
        
        # Verificar si hay errores del lado del servidor PRIMERO
        try:
            server_error = driver.find_element(By.CSS_SELECTOR, ".alert-danger")
            print("✗ ERROR DEL SERVIDOR:")
            print(f"  {server_error.text}")
            
            # Buscar errores específicos de campos (Django los muestra como divs con class text-danger)
            print("\n  Buscando errores específicos de campos...")
            
            # Buscar todos los divs con clase text-danger
            field_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger.small")
            if field_errors:
                print("  Errores de validación encontrados:")
                for error in field_errors:
                    error_text = error.text.strip()
                    if error_text:
                        # Buscar el label del campo asociado
                        try:
                            parent = error.find_element(By.XPATH, "..")
                            label = parent.find_element(By.CSS_SELECTOR, "label")
                            campo = label.text
                            print(f"    - {campo}: {error_text}")
                        except:
                            print(f"    - {error_text}")
            else:
                print("  No se encontraron errores específicos de campos visibles")
            
            # Buscar errorlist (otra forma de Django mostrar errores)
            errorlists = driver.find_elements(By.CSS_SELECTOR, ".errorlist")
            if errorlists:
                print("\n  Errorlists encontradas:")
                for el in errorlists:
                    if el.text.strip():
                        print(f"    - {el.text}")
            
            # Imprimir todo el HTML del formulario para debug
            print("\n  Capturando HTML del área de errores...")
            try:
                form_html = driver.find_element(By.TAG_NAME, "form").get_attribute("outerHTML")
                # Buscar líneas que contengan "text-danger" o "error"
                for line in form_html.split("\n"):
                    if "text-danger" in line or "errorlist" in line:
                        print(f"    HTML: {line.strip()[:200]}")
            except:
                pass
            
            # Mantenernos en el formulario para inspección manual
            time.sleep(15)
            return False
            
        except NoSuchElementException:
            pass  # No hay errores visibles
        
        # Esperar procesamiento y redirección
        time.sleep(2)
        
        # Verificar cookies de sesión
        cookies = driver.get_cookies()
        session_cookie = None
        for cookie in cookies:
            if cookie['name'] == 'sessionid':
                session_cookie = cookie
                break
        
        if session_cookie:
            print(f"✓ Cookie de sesión presente")
        else:
            print("⚠ No se encontró cookie de sesión")
        
        # Verificar si hay errores en el formulario
        try:
            error_alert = driver.find_element(By.CSS_SELECTOR, ".alert-danger")
            print("✗ ERROR: Se encontraron errores en el formulario")
            print(f"  Mensaje: {error_alert.text}")
            
            # Buscar errores específicos de campos
            field_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
            if field_errors:
                print("\n  Errores de campos:")
                for error in field_errors:
                    if error.text.strip():
                        print(f"    - {error.text}")
            
            return False
            
        except NoSuchElementException:
            print("✓ No se encontraron errores en el formulario")
        
        # Verificar mensaje de éxito o redirección
        current_url = driver.current_url
        print(f"\n  URL actual: {current_url}")
        
        # La URL de detalle puede ser /pacientes/<id>/ o /pacientes/detalle/<id>/
        if "/pacientes/" in current_url and current_url != "http://127.0.0.1:8000/pacientes/crear/":
            print("✓ Redirección exitosa después de crear paciente")
            
            # Buscar mensaje de éxito
            try:
                success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success, .alert-info")
                print(f"✓ Mensaje de éxito: {success_message.text}")
            except NoSuchElementException:
                print("  (No se encontró mensaje de éxito explícito, pero hubo redirección)")
            
            print("\n" + "=" * 80)
            print("✓ TEST EXITOSO: PACIENTE CREADO CORRECTAMENTE")
            print("=" * 80)
            print(f"\nPaciente creada:")
            print(f"  - RUT: {rut_paciente}")
            print(f"  - Nombre: María Isabel González Pérez")
            print(f"  - Edad: 25 años")
            print(f"  - Previsión: FONASA B")
            print(f"  - Comuna: Chillán, Región de Ñuble")
            
            return True
            
        else:
            print(f"⚠ ADVERTENCIA: URL inesperada después de enviar: {current_url}")
            print("  Se esperaba redirección a detalle o búsqueda de paciente")
            
            # Verificar si seguimos en el formulario (puede indicar error)
            if "/pacientes/crear/" in current_url:
                print("  ⚠ Seguimos en el formulario de creación")
                print("  Buscando errores no detectados...")
                
                # Buscar cualquier mensaje de error
                all_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger, .alert-danger, .invalid-feedback")
                if all_errors:
                    print("\n  Errores encontrados:")
                    for error in all_errors:
                        if error.text.strip():
                            print(f"    - {error.text}")
                    return False
            
            return False
    
    except TimeoutException as e:
        print(f"\n✗ ERROR: Timeout esperando elemento")
        print(f"  Detalle: {str(e)}")
        print(f"  URL actual: {driver.current_url}")
        return False
        
    except Exception as e:
        print(f"\n✗ ERROR INESPERADO: {str(e)}")
        print(f"  Tipo: {type(e).__name__}")
        print(f"  URL actual: {driver.current_url}")
        
        # Intentar capturar errores del formulario
        try:
            errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger, .alert-danger")
            if errors:
                print("\n  Errores en el formulario:")
                for error in errors:
                    if error.text.strip():
                        print(f"    - {error.text}")
        except:
            pass
        
        return False
        
    finally:
        # Mantener navegador abierto brevemente para ver resultado
        print("\nManteniendo navegador abierto 3 segundos...")
        time.sleep(3)
        driver.quit()
        print("Navegador cerrado.")


def verificar_paciente_en_base_datos(rut):
    """
    Verifica que el paciente se haya guardado correctamente en la base de datos.
    """
    import os
    import django
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
    django.setup()
    
    from apps.pacientes.models import PacienteMadre
    
    try:
        paciente = PacienteMadre.objects.get(rut=rut)
        print("\n" + "=" * 80)
        print("VERIFICACIÓN EN BASE DE DATOS")
        print("=" * 80)
        print(f"✓ Paciente encontrado en base de datos")
        print(f"  - ID: {paciente.id}")
        print(f"  - RUT: {paciente.rut}")
        print(f"  - Nombre completo: {paciente.nombre_completo}")
        print(f"  - Edad: {paciente.edad} años")
        print(f"  - Estado Civil: {paciente.get_estado_civil_display()}")
        print(f"  - Escolaridad: {paciente.get_escolaridad_display()}")
        print(f"  - Previsión: {paciente.get_prevision_display()}")
        print(f"  - Comuna: {paciente.comuna}")
        print(f"  - Región: {paciente.region}")
        print(f"  - Teléfono: {paciente.telefono}")
        print(f"  - Fecha creación: {paciente.created_at}")
        return True
        
    except PacienteMadre.DoesNotExist:
        print(f"\n✗ ERROR: No se encontró el paciente con RUT {rut} en la base de datos")
        return False


if __name__ == "__main__":
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "TEST SELENIUM - CREAR PACIENTE" + " " * 27 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\nEste test automatiza el formulario de creación de paciente madre.")
    print("Requisito: El servidor debe estar corriendo en http://127.0.0.1:8000")
    print("\nPresione Ctrl+C para cancelar...\n")
    
    try:
        time.sleep(2)
        resultado = test_crear_paciente()
        
        if resultado:
            print("\n✓ Test completado exitosamente")
            exit(0)
        else:
            print("\n✗ Test falló")
            exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelado por el usuario")
        exit(1)
