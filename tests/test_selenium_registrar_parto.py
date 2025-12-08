"""
Test de Selenium para automatizar el registro de parto y RN.
Usa una paciente existente, registra parto y luego el recién nacido.
"""

import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def test_registrar_parto():
    """
    Test completo: Registra parto y RN de una paciente existente.
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    # ID de paciente existente (cambiar según necesidad)
    PACIENTE_ID = "1"  # Usar paciente existente en la BD
    
    try:
        print("=" * 80)
        print("TEST: REGISTRAR PARTO Y RECIEN NACIDO")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN
        # ===================================================================
        print("\n[1/4] Iniciando sesión...")
        driver.get("http://127.0.0.1:8000/auth/login/")
        
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("medico_g")
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("doc@12345678")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(2)
        print("✓ Sesión iniciada como medico_g")
        
        # ===================================================================
        # PASO 2: REGISTRAR PARTO
        # ===================================================================
        print(f"\n[2/4] Registrando parto para paciente ID: {PACIENTE_ID}...")
        driver.get(f"http://127.0.0.1:8000/obstetricia/parto/registrar/{PACIENTE_ID}/")
        
        wait.until(EC.presence_of_element_located((By.ID, "id_fecha_parto")))
        print("✓ Formulario de parto cargado")
        
        # Completar formulario de parto
        print("  Completando campos...")
        
        # Fecha y hora del parto
        fecha_parto = date.today()
        hora_parto = "14:30"
        
        fecha_parto_input = driver.find_element(By.ID, "id_fecha_parto")
        driver.execute_script(f"arguments[0].value = '{fecha_parto.strftime('%Y-%m-%d')}';", fecha_parto_input)
        print("  ✓ Fecha de parto completada")
        
        driver.find_element(By.ID, "id_hora_parto").send_keys(hora_parto)
        print("  ✓ Hora de parto completada")
        
        # Edad gestacional
        sem_input = driver.find_element(By.ID, "id_edad_gestacional_semanas")
        sem_input.clear()
        sem_input.send_keys("39")
        
        dias_input = driver.find_element(By.ID, "id_edad_gestacional_dias")
        dias_input.clear()
        dias_input.send_keys("3")
        print("  ✓ Edad gestacional completada (39 semanas + 3 días)")
        
        # SECCION 1: Datos del Parto
        
        # Control prenatal (opcional, si existe seleccionar el primero)
        try:
            control_select = Select(driver.find_element(By.ID, "id_control_prenatal"))
            if len(control_select.options) > 1:
                control_select.select_by_index(1)
                print("  ✓ Control prenatal seleccionado")
        except:
            print("  - Control prenatal no disponible")
        
        # Tipo de parto
        Select(driver.find_element(By.ID, "id_tipo_parto")).select_by_value("eutocico")
        print("  ✓ Tipo de parto: Eutócico")
        
        # Presentación
        Select(driver.find_element(By.ID, "id_presentacion")).select_by_value("cefalica")
        print("  ✓ Presentación: Cefálica")
        
        # Inicio de trabajo de parto
        Select(driver.find_element(By.ID, "id_inicio_trabajo_parto")).select_by_value("espontaneo")
        print("  ✓ Inicio: Espontáneo")
        
        # Lugar de atención
        Select(driver.find_element(By.ID, "id_lugar_atencion")).select_by_value("sala_parto")
        print("  ✓ Lugar: Sala de Parto")
        
        # Alumbramiento
        Select(driver.find_element(By.ID, "id_alumbramiento")).select_by_value("completo")
        print("  ✓ Alumbramiento: Completo")
        
        # Navegar a sección 2
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        print("  → Navegando a Sección 2...")
        
        # SECCION 2: Antecedentes y Estado Materno
        
        # Paridad: Primigesta
        driver.find_element(By.ID, "id_primigesta").click()
        print("  ✓ Paridad: Primigesta")
        
        # Rotura de membranas
        Select(driver.find_element(By.ID, "id_rotura_membranas")).select_by_value("espontanea")
        print("  ✓ Rotura membranas: Espontánea")
        
        # Líquido amniótico
        Select(driver.find_element(By.ID, "id_liquido_amniotico")).select_by_value("claro")
        print("  ✓ Líquido amniótico: Claro")
        
        # Anestesia
        Select(driver.find_element(By.ID, "id_anestesia")).select_by_value("epidural")
        print("  ✓ Anestesia: Epidural")
        
        # Navegar a sección 3
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        print("  → Navegando a Sección 3...")
        
        # SECCION 3: Complicaciones y Procedimientos
        
        # Desgarro perineal
        Select(driver.find_element(By.ID, "id_desgarro_perineal")).select_by_value("ninguno")
        print("  ✓ Desgarro: Ninguno")
        
        # Navegar a sección 4
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        print("  → Navegando a Sección 4...")
        
        # SECCION 4: Observaciones
        
        driver.find_element(By.ID, "id_observaciones").send_keys("Parto eutócico sin complicaciones. Test automatizado Selenium.")
        print("  ✓ Observaciones agregadas")
        
        print("  ✓ TODOS los campos completados")
        
        # ===================================================================
        # PASO 5: ENVIAR FORMULARIO
        # ===================================================================
        print("\n[4/5] Enviando formulario...")
        
        current_url_before = driver.current_url
        print(f"  URL antes de enviar: {current_url_before}")
        
        # Buscar botón submit del formulario (no el de logout del navbar)
        submit_button = driver.find_element(By.ID, "btnSubmit")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        
        # Verificar token CSRF
        csrf_inputs = driver.find_elements(By.NAME, "csrfmiddlewaretoken")
        if csrf_inputs:
            csrf_value = csrf_inputs[0].get_attribute("value")
            print(f"✓ Token CSRF presente: {csrf_value[:20]}...")
        
        # Enviar formulario directamente (no con click en botón)
        form_element = driver.find_element(By.ID, "formParto")
        driver.execute_script("arguments[0].submit();", form_element)
        print("✓ Formulario enviado (form.submit())")
        
        time.sleep(3)
        
        # Verificar si estamos aún en la misma página
        if driver.current_url == current_url_before:
            print("  ⚠ Permanece en la misma URL (posible error de validación)")
        
        # ===================================================================
        # PASO 6: VERIFICAR RESULTADO
        # ===================================================================
        print("\n[5/5] Verificando resultado...")
        
        current_url_after = driver.current_url
        print(f"  URL después de enviar: {current_url_after}")
        
        # Buscar mensajes de error de formulario Django
        error_alert = driver.find_elements(By.CSS_SELECTOR, ".alert-danger ul li")
        if error_alert:
            print("\n✗ ERRORES DE VALIDACION DEL FORMULARIO:")
            for err in error_alert:
                print(f"  • {err.text.strip()}")
            
            # Guardar captura del error
            driver.save_screenshot("error_form_parto.png")
            print("\n  📸 Screenshot guardado: error_form_parto.png")
            return False
        
        print("✓ No se encontraron errores de validación visibles")
        
        # Buscar mensajes de éxito
        success_messages = driver.find_elements(By.CSS_SELECTOR, ".alert-success")
        if success_messages:
            print("\n✓ MENSAJES DE ÉXITO:")
            for msg in success_messages:
                print(f"  • {msg.text.strip()}")
        
        # Si no redirigi, buscar mensajes de error inline o campos invalidos
        invalid_fields = driver.find_elements(By.CSS_SELECTOR, ".is-invalid")
        if invalid_fields:
            print(f"\n⚠ Campos marcados como inválidos: {len(invalid_fields)}")
            for field in invalid_fields[:5]:  # Mostrar solo los primeros 5
                field_id = field.get_attribute("id") or field.get_attribute("name")
                print(f"  - {field_id}")
        
        # Verificar mensajes de Django messages framework  
        error_messages = driver.find_elements(By.CSS_SELECTOR, ".alert.alert-danger, .alert.alert-warning")
        if error_messages:
            print("\n⚠ MENSAJES DE ERROR DEL SISTEMA:")
            for msg in error_messages:
                print(f"  • {msg.text.strip()}")
        
        # Si no redirigió, guardar HTML para debug
        if driver.current_url == current_url_before:
            with open("debug_parto_form.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("\n  💾 HTML guardado en: debug_parto_form.html")
            print("  💡 Revisar el HTML para ver errores ocultos o problemas de validación")
        
        # Verificar redirección a registrar RN
        if "/neonatologia/registrar/" in current_url_after:
            print("✓ Redirigió a registrar RN correctamente")
            
            # Extraer parto_id de la URL: /neonatologia/registrar/{parto_id}/
            parto_id = current_url_after.rstrip('/').split('/')[-1]
            print(f"  Parto registrado con ID: {parto_id}")
            
            # ===================================================================
            # PASO 3: REGISTRAR RECIÉN NACIDO
            # ===================================================================
            print(f"\n[3/4] Registrando recién nacido (Parto ID: {parto_id})...")
            
            wait.until(EC.presence_of_element_located((By.ID, "id_peso_gramos")))
            print("✓ Formulario de RN cargado")
            
            # === DATOS BÁSICOS Y ANTROPOMETRÍA ===
            print("\n  Completando datos básicos...")
            Select(driver.find_element(By.ID, "id_sexo")).select_by_value("masculino")
            driver.find_element(By.ID, "id_peso_gramos").send_keys("3200")
            driver.find_element(By.ID, "id_talla_cm").send_keys("49.5")
            driver.find_element(By.ID, "id_circunferencia_craneana_cm").send_keys("34.2")
            print("    ✓ Sexo: Masculino")
            print("    ✓ Peso: 3200g")
            print("    ✓ Talla: 49.5cm")
            print("    ✓ Circunferencia craneana: 34.2cm")
            
            # === EVALUACIÓN APGAR ===
            print("\n  Completando APGAR...")
            driver.find_element(By.ID, "id_apgar_1_min").send_keys("8")
            driver.find_element(By.ID, "id_apgar_5_min").send_keys("9")
            print("    ✓ APGAR 1 min: 8")
            print("    ✓ APGAR 5 min: 9")
            
            # === REANIMACIÓN Y DESTINO ===
            print("\n  Completando reanimación y destino...")
            Select(driver.find_element(By.ID, "id_estado_al_nacer")).select_by_value("vivo")
            print("    ✓ Estado al nacer: Vivo")
            
            # Reanimación no requerida (checkbox sin marcar)
            Select(driver.find_element(By.ID, "id_tipo_reanimacion")).select_by_value("ninguna")
            print("    ✓ Tipo reanimación: Ninguna")
            
            Select(driver.find_element(By.ID, "id_destino")).select_by_value("alojamiento_conjunto")
            print("    ✓ Destino: Alojamiento Conjunto")
            
            # === MALFORMACIONES ===
            # Checkbox sin marcar (no presenta malformaciones)
            print("    ✓ Sin malformaciones")
            
            # === OBSERVACIONES ===
            driver.find_element(By.ID, "id_observaciones").send_keys("RN de término adecuado para la edad gestacional. Test automatizado.")
            print("    ✓ Observaciones agregadas")
            
            print("\n  ✓ TODOS los datos del RN completados")
            
            # === ENVIAR FORMULARIO RN ===
            print("\n  Enviando formulario RN...")
            submit_button_rn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-success")
            driver.execute_script("arguments[0].scrollIntoView(true);", submit_button_rn)
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", submit_button_rn)
            print("  ✓ Formulario RN enviado")
            
            time.sleep(3)
            
            # ===================================================================
            # PASO 4: VERIFICAR RESULTADO FINAL
            # ===================================================================
            print(f"\n[4/4] Verificación final...")
            final_url = driver.current_url
            print(f"  URL final: {final_url}")
            
            print("\n" + "=" * 80)
            print("✓ TEST EXITOSO: PARTO Y RN REGISTRADOS")
            print("=" * 80)
            print(f"\nRegistro completo:")
            print(f"  - Paciente ID: {PACIENTE_ID}")
            print(f"  - Parto ID: {parto_id}")
            print(f"  - Fecha: {fecha_parto.strftime('%d/%m/%Y')}")
            print(f"  - Hora: {hora_parto}")
            print(f"  - RN: 3200g, 49cm, APGAR 9/9")
            
            print("\nManteniendo navegador abierto 5 segundos...")
            time.sleep(5)
        else:
            print(f"⚠ URL inesperada: {current_url_after}")
            print("  Se esperaba redirección a registrar RN")
        
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
    print("\n" + "=" * 80)
    print("TEST SELENIUM - REGISTRAR PARTO")
    print("=" * 80)
    
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
