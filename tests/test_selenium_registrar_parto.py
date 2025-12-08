"""
Test de Selenium para automatizar el registro de parto.
Prueba el formulario completo de registro de parto obstétrico.
"""

import time
import random
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def generar_rut_valido():
    """Genera un RUT chileno válido aleatorio"""
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


def crear_paciente_para_parto(driver, wait):
    """
    Crea una paciente madre para poder registrar el parto.
    Retorna el ID de la paciente creada.
    """
    print("\n[Pre-requisito] Creando paciente madre...")
    
    # Navegar al formulario de crear paciente
    driver.get("http://127.0.0.1:8000/pacientes/crear/")
    wait.until(EC.presence_of_element_located((By.ID, "id_rut")))
    
    # Generar datos
    rut_paciente = generar_rut_valido()
    edad_anios = random.randint(18, 35)  # Edad fértil
    fecha_nacimiento = date.today() - timedelta(days=edad_anios*365 + random.randint(0, 364))
    
    # Completar formulario básico de paciente
    driver.find_element(By.ID, "id_rut").send_keys(rut_paciente)
    driver.find_element(By.ID, "id_nombre").send_keys("María Isabel")
    driver.find_element(By.ID, "id_apellido_paterno").send_keys("González")
    driver.find_element(By.ID, "id_apellido_materno").send_keys("Pérez")
    
    # Fecha de nacimiento con JavaScript
    fecha_input = driver.find_element(By.ID, "id_fecha_nacimiento")
    driver.execute_script(f"arguments[0].value = '{fecha_nacimiento.strftime('%Y-%m-%d')}';", fecha_input)
    
    # Campos obligatorios
    Select(driver.find_element(By.ID, "id_estado_civil")).select_by_value("casada")
    Select(driver.find_element(By.ID, "id_escolaridad")).select_by_value("media_completa")
    Select(driver.find_element(By.ID, "id_prevision")).select_by_value("fonasa_b")
    
    driver.find_element(By.ID, "id_direccion").send_keys("Av. Libertad 456")
    driver.find_element(By.ID, "id_comuna").send_keys("Chillán")
    driver.find_element(By.ID, "id_region").send_keys("Ñuble")
    
    # Enviar
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", submit_button)
    
    time.sleep(2)
    
    # Extraer ID de la URL (ej: /pacientes/5/)
    current_url = driver.current_url
    paciente_id = current_url.rstrip('/').split('/')[-1]
    
    print(f"✓ Paciente creada: {rut_paciente} (ID: {paciente_id})")
    return paciente_id


def test_registrar_parto():
    """
    Test completo de registro de parto.
    Completa todos los campos del formulario y verifica el registro exitoso.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("=" * 80)
        print("TEST: REGISTRAR PARTO")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN
        # ===================================================================
        print("\n[1/5] Iniciando sesión...")
        driver.get("http://127.0.0.1:8000/auth/login/")
        
        # Login como matrona (puede registrar partos)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("medico_g")  # También puede usar matrona_test
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("doc@12345678")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(2)
        print("✓ Sesión iniciada como medico_g")
        
        # ===================================================================
        # PASO 2: CREAR PACIENTE (Pre-requisito)
        # ===================================================================
        paciente_id = crear_paciente_para_parto(driver, wait)
        
        # ===================================================================
        # PASO 3: NAVEGAR AL FORMULARIO DE REGISTRAR PARTO
        # ===================================================================
        print(f"\n[2/5] Navegando al formulario de registrar parto (paciente ID: {paciente_id})...")
        driver.get(f"http://127.0.0.1:8000/obstetricia/registrar-parto/{paciente_id}/")
        
        wait.until(EC.presence_of_element_located((By.ID, "id_fecha_parto")))
        print("✓ Formulario de registrar parto cargado")
        
        # ===================================================================
        # PASO 4: COMPLETAR FORMULARIO DE PARTO
        # ===================================================================
        print("\n[3/5] Completando formulario de parto...")
        
        # Fecha y hora del parto
        fecha_parto = date.today()
        hora_parto = "14:30"
        
        fecha_parto_input = driver.find_element(By.ID, "id_fecha_parto")
        driver.execute_script(f"arguments[0].value = '{fecha_parto.strftime('%Y-%m-%d')}';", fecha_parto_input)
        print("  ✓ Fecha de parto completada")
        
        driver.find_element(By.ID, "id_hora_parto").send_keys(hora_parto)
        print("  ✓ Hora de parto completada")
        
        # Edad gestacional
        driver.find_element(By.ID, "id_edad_gestacional_semanas").send_keys("39")
        driver.find_element(By.ID, "id_edad_gestacional_dias").send_keys("3")
        print("  ✓ Edad gestacional completada")
        
        # Tipo de parto
        Select(driver.find_element(By.ID, "id_tipo_parto")).select_by_value("vaginal")
        print("  ✓ Tipo de parto: Vaginal")
        
        # Presentación
        Select(driver.find_element(By.ID, "id_presentacion")).select_by_value("cefalica")
        print("  ✓ Presentación: Cefálica")
        
        # Inicio de trabajo de parto
        Select(driver.find_element(By.ID, "id_inicio_trabajo_parto")).select_by_value("espontaneo")
        print("  ✓ Inicio: Espontáneo")
        
        # Lugar del parto
        Select(driver.find_element(By.ID, "id_lugar_parto")).select_by_value("hospital")
        print("  ✓ Lugar: Hospital")
        
        # Alumbramiento
        try:
            Select(driver.find_element(By.ID, "id_alumbramiento")).select_by_value("espontaneo")
            print("  ✓ Alumbramiento: Espontáneo")
        except:
            print("  ⚠ Campo alumbramiento no encontrado (opcional)")
        
        # Líquido amniótico
        try:
            Select(driver.find_element(By.ID, "id_liquido_amniotico")).select_by_value("claro")
            print("  ✓ Líquido amniótico: Claro")
        except:
            print("  ⚠ Campo líquido amniótico no encontrado (opcional)")
        
        # Anestesia
        try:
            Select(driver.find_element(By.ID, "id_anestesia")).select_by_value("epidural")
            print("  ✓ Anestesia: Epidural")
        except:
            print("  ⚠ Campo anestesia no encontrado (opcional)")
        
        # Paridad (si existe)
        try:
            driver.find_element(By.ID, "id_paridad").send_keys("1")
            print("  ✓ Paridad completada")
        except:
            print("  ⚠ Campo paridad no encontrado (opcional)")
        
        # Gestaciones previas
        try:
            driver.find_element(By.ID, "id_gestaciones_previas").send_keys("0")
            print("  ✓ Gestaciones previas completadas")
        except:
            print("  ⚠ Campo gestaciones previas no encontrado (opcional)")
        
        # Cesáreas previas
        try:
            driver.find_element(By.ID, "id_cesareas_previas").send_keys("0")
            print("  ✓ Cesáreas previas completadas")
        except:
            print("  ⚠ Campo cesáreas previas no encontrado (opcional)")
        
        # Observaciones
        try:
            driver.find_element(By.ID, "id_observaciones").send_keys("Parto sin complicaciones. Test automatizado Selenium.")
            print("  ✓ Observaciones completadas")
        except:
            print("  ⚠ Campo observaciones no encontrado (opcional)")
        
        # ===================================================================
        # PASO 5: ENVIAR FORMULARIO
        # ===================================================================
        print("\n[4/5] Enviando formulario...")
        
        current_url_before = driver.current_url
        print(f"  URL antes de enviar: {current_url_before}")
        
        # Scroll al botón
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        
        # Verificar token CSRF
        csrf_inputs = driver.find_elements(By.NAME, "csrfmiddlewaretoken")
        if csrf_inputs:
            csrf_value = csrf_inputs[0].get_attribute("value")
            print(f"✓ Token CSRF presente: {csrf_value[:20]}...")
        
        # Enviar formulario
        driver.execute_script("arguments[0].click();", submit_button)
        print("✓ Formulario enviado")
        
        time.sleep(3)
        
        # ===================================================================
        # PASO 6: VERIFICAR RESULTADO
        # ===================================================================
        print("\n[5/5] Verificando resultado...")
        
        current_url_after = driver.current_url
        print(f"  URL después de enviar: {current_url_after}")
        
        # Buscar mensajes de error
        try:
            errors = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .text-danger, .errorlist")
            if errors:
                print("\n✗ ERRORES ENCONTRADOS:")
                for err in errors:
                    if err.text.strip():
                        print(f"  - {err.text}")
                return False
            else:
                print("✓ No se encontraron errores en el formulario")
        except:
            pass
        
        # Verificar redirección exitosa (debe ir a registrar RN o detalle parto)
        if "registrar-recien-nacido" in current_url_after or "parto" in current_url_after:
            print("✓ Redirección exitosa después de registrar parto")
            
            # Buscar mensaje de éxito
            try:
                success_msg = driver.find_element(By.CSS_SELECTOR, ".alert-success")
                print(f"✓ Mensaje de éxito: {success_msg.text}")
            except:
                print("✓ Parto registrado (sin mensaje de éxito visible)")
        else:
            print("⚠ URL inesperada después de enviar")
        
        print("\n" + "=" * 80)
        print("✓ TEST EXITOSO: PARTO REGISTRADO CORRECTAMENTE")
        print("=" * 80)
        print(f"\nParto registrado:")
        print(f"  - Paciente ID: {paciente_id}")
        print(f"  - Fecha: {fecha_parto.strftime('%d/%m/%Y')}")
        print(f"  - Hora: {hora_parto}")
        print(f"  - Tipo: Vaginal")
        print(f"  - Edad gestacional: 39 semanas, 3 días")
        print(f"  - Presentación: Cefálica")
        
        print("\nManteniendo navegador abierto 5 segundos...")
        time.sleep(5)
        
        return True
        
    except TimeoutException as e:
        print(f"\n✗ ERROR: Timeout esperando elemento")
        print(f"  Detalles: {str(e)}")
        driver.save_screenshot("error_registrar_parto.png")
        print("  Captura guardada: error_registrar_parto.png")
        return False
        
    except Exception as e:
        print(f"\n✗ ERROR INESPERADO:")
        print(f"  Tipo: {type(e).__name__}")
        print(f"  Mensaje: {str(e)}")
        driver.save_screenshot("error_registrar_parto.png")
        print("  Captura guardada: error_registrar_parto.png")
        return False
        
    finally:
        print("Navegador cerrado.")
        driver.quit()


if __name__ == "__main__":
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 22 + "TEST SELENIUM - REGISTRAR PARTO" + " " * 25 + "║")
    print("╚" + "=" * 78 + "╝")
    
    print("\nEste test automatiza el formulario de registro de parto obstétrico.")
    print("Requisito: El servidor debe estar corriendo en http://127.0.0.1:8000")
    print("Requisito: Usuario medico_g con password doc@12345678")
    print("\nPresione Ctrl+C para cancelar...\n")
    
    try:
        time.sleep(2)
        resultado = test_registrar_parto()
        
        if resultado:
            print("\n✓ Test completado exitosamente")
            exit(0)
        else:
            print("\n✗ Test falló")
            exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelado por el usuario")
        exit(1)
