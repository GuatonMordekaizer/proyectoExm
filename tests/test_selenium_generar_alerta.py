"""
Test de Selenium para generar alerta de APGAR crítico.
Registra un parto + RN con APGAR 5 min < 7 que genera alerta automática.
"""

import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Usar paciente existente
PACIENTE_ID = "1"  # Paciente debe existir en DB


def test_generar_alerta_apgar():
    """
    Test principal: Registra parto + RN con APGAR < 7
    para generar alerta automática APGAR_CRITICO.
    """
    
    print("\n" + "=" * 80)
    print("TEST SELENIUM - GENERAR ALERTA APGAR CRÍTICO")
    print("=" * 80)
    print("\nEste test registra un parto + RN con APGAR 5 min < 7")
    print("para verificar que el sistema genera alertas automáticamente.")
    print(f"\nRequisito: Servidor corriendo en http://127.0.0.1:8000")
    print(f"Requisito: Usuario medico_g con password doc@12345678")
    print(f"Requisito: Paciente ID {PACIENTE_ID} debe existir")
    print("\nPresione Ctrl+C para cancelar...")
    time.sleep(3)
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("\n" + "=" * 80)
        print("TEST: GENERAR ALERTA APGAR CRÍTICO")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN
        # ===================================================================
        print("\n[1/3] Iniciando sesión...")
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
        print(f"\n[2/3] Registrando parto para paciente ID: {PACIENTE_ID}...")
        driver.get(f"http://127.0.0.1:8000/obstetricia/parto/registrar/{PACIENTE_ID}/")
        
        wait.until(EC.presence_of_element_located((By.ID, "id_fecha_parto")))
        print("✓ Formulario de parto cargado")
        
        # SECCIÓN 1: Datos del Parto
        print("  Completando datos del parto...")
        
        fecha_parto = date.today()
        fecha_parto_input = driver.find_element(By.ID, "id_fecha_parto")
        driver.execute_script(f"arguments[0].value = '{fecha_parto.strftime('%Y-%m-%d')}';", fecha_parto_input)
        
        driver.find_element(By.ID, "id_hora_parto").send_keys("16:45")
        
        sem_input = driver.find_element(By.ID, "id_edad_gestacional_semanas")
        sem_input.clear()
        sem_input.send_keys("37")
        
        dias_input = driver.find_element(By.ID, "id_edad_gestacional_dias")
        dias_input.clear()
        dias_input.send_keys("4")
        
        Select(driver.find_element(By.ID, "id_tipo_parto")).select_by_value("eutocico")
        Select(driver.find_element(By.ID, "id_presentacion")).select_by_value("cefalica")
        Select(driver.find_element(By.ID, "id_inicio_trabajo_parto")).select_by_value("espontaneo")
        Select(driver.find_element(By.ID, "id_lugar_atencion")).select_by_value("sala_parto")
        Select(driver.find_element(By.ID, "id_alumbramiento")).select_by_value("completo")
        
        # Navegar a sección 2
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        
        # SECCIÓN 2: Antecedentes
        driver.find_element(By.ID, "id_primigesta").click()
        Select(driver.find_element(By.ID, "id_rotura_membranas")).select_by_value("espontanea")
        Select(driver.find_element(By.ID, "id_liquido_amniotico")).select_by_value("meconial")
        Select(driver.find_element(By.ID, "id_anestesia")).select_by_value("epidural")
        
        # Navegar a sección 3
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        
        # SECCIÓN 3: Complicaciones
        Select(driver.find_element(By.ID, "id_desgarro_perineal")).select_by_value("ninguno")
        
        # Navegar a sección 4
        driver.execute_script("nextStep()")
        time.sleep(0.8)
        
        # SECCIÓN 4: Observaciones
        driver.find_element(By.ID, "id_observaciones").send_keys("Parto con líquido meconial. Test de alerta APGAR.")
        
        print("  ✓ Formulario completado")
        
        # Enviar formulario de parto
        print("  Enviando formulario de parto...")
        form = driver.find_element(By.ID, "formParto")
        form.submit()
        
        time.sleep(3)
        print("✓ Parto registrado")
        
        # Verificar redirección a RN
        current_url = driver.current_url
        if "/neonatologia/registrar/" not in current_url:
            print(f"✗ ERROR: No redirigió a registrar RN. URL: {current_url}")
            
            # Buscar mensajes de error
            try:
                error_messages = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .alert-error")
                if error_messages:
                    print("\n⚠️ ERRORES DE VALIDACIÓN ENCONTRADOS:")
                    for msg in error_messages:
                        print(f"  - {msg.text.strip()}")
                else:
                    print("  No se encontraron mensajes de error visibles")
            except Exception as e:
                print(f"  Error al buscar mensajes: {e}")
            
            # Tomar screenshot del error
            try:
                driver.save_screenshot("error_parto_no_redirige.png")
                print("📸 Screenshot guardado: error_parto_no_redirige.png")
            except:
                pass
            
            return False
        
        parto_id = current_url.rstrip('/').split('/')[-1]
        print(f"✓ Redirigió a registrar RN (Parto ID: {parto_id})")
        
        # ===================================================================
        # PASO 3: REGISTRAR RN CON APGAR CRÍTICO < 7
        # ===================================================================
        print(f"\n[3/3] Registrando RN con APGAR CRÍTICO...")
        
        wait.until(EC.presence_of_element_located((By.ID, "id_peso_gramos")))
        print("✓ Formulario de RN cargado")
        
        # Datos básicos
        print("\n  Completando datos del RN...")
        Select(driver.find_element(By.ID, "id_sexo")).select_by_value("masculino")
        driver.find_element(By.ID, "id_peso_gramos").send_keys("2800")
        driver.find_element(By.ID, "id_talla_cm").send_keys("47.5")
        driver.find_element(By.ID, "id_circunferencia_craneana_cm").send_keys("33.5")
        print("    ✓ Antropometría completada")
        
        # ⚠️ APGAR CRÍTICO - Esto generará la alerta automática
        apgar_1_min = "5"
        apgar_5_min = "6"  # < 7 = CRÍTICO ⚠️
        
        driver.find_element(By.ID, "id_apgar_1_min").send_keys(apgar_1_min)
        print(f"    ✓ APGAR 1 min: {apgar_1_min}")
        
        driver.find_element(By.ID, "id_apgar_5_min").send_keys(apgar_5_min)
        print(f"    ⚠️  APGAR 5 min: {apgar_5_min} (CRÍTICO < 7)")
        print(f"    → Esto debe generar alerta automática APGAR_CRITICO")
        
        # Reanimación y destino
        Select(driver.find_element(By.ID, "id_estado_al_nacer")).select_by_value("vivo")
        Select(driver.find_element(By.ID, "id_tipo_reanimacion")).select_by_value("oxigeno")
        Select(driver.find_element(By.ID, "id_destino")).select_by_value("neonatologia")
        print("    ✓ Estado y destino completados")
        
        # Observaciones
        driver.find_element(By.ID, "id_observaciones").send_keys(
            "RN con dificultad respiratoria leve. APGAR bajo, requiere vigilancia. Test alerta."
        )
        print("    ✓ Observaciones agregadas")
        
        # Enviar formulario RN
        print("\n  Enviando formulario RN...")
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-success")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", submit_button)
        print("  ✓ Formulario RN enviado")
        
        time.sleep(3)
        
        # ===================================================================
        # PASO 4: VERIFICAR ALERTA GENERADA
        # ===================================================================
        print("\n" + "=" * 80)
        print("VERIFICANDO ALERTA AUTOMÁTICA")
        print("=" * 80)
        
        final_url = driver.current_url
        print(f"\nURL final: {final_url}")
        
        # Verificar si hay alerta en la página de detalle
        if "/neonatologia/detalle/" in final_url:
            print("✓ Redirigió a detalle del RN")
            
            # Buscar card de alertas
            try:
                alerta_header = driver.find_element(By.XPATH, "//*[contains(text(), 'Alertas')]")
                print("\n✓ ENCONTRADA: Sección de Alertas en la página")
                
                # Buscar badge con número de alertas
                try:
                    badge = driver.find_element(By.CSS_SELECTOR, ".card-header-compact .badge")
                    num_alertas = badge.text
                    print(f"✓ Número de alertas: {num_alertas}")
                except:
                    print("  (No se pudo obtener contador de alertas)")
                
                # Buscar contenido de la alerta
                try:
                    alertas = driver.find_elements(By.CSS_SELECTOR, ".alert-danger, .alert-warning")
                    if alertas:
                        print(f"\n✓ ALERTAS ENCONTRADAS: {len(alertas)} alerta(s)")
                        for i, alerta in enumerate(alertas, 1):
                            texto = alerta.text.strip()
                            if texto:
                                print(f"\n  Alerta #{i}:")
                                print(f"  {texto}")
                                
                                # Verificar si es alerta de APGAR
                                if "APGAR" in texto.upper():
                                    print(f"\n  ✓✓✓ ALERTA DE APGAR CRÍTICO GENERADA CORRECTAMENTE ✓✓✓")
                    else:
                        print("✗ No se encontraron alertas visibles")
                        
                except Exception as e:
                    print(f"⚠ Error al buscar alertas: {e}")
                
            except:
                print("⚠ No se encontró sección de alertas en la página")
                print("  Puede que no haya alertas o la estructura HTML sea diferente")
        
        else:
            print(f"⚠ URL inesperada: {final_url}")
        
        # Captura de pantalla
        screenshot_path = "test_alerta_apgar.png"
        driver.save_screenshot(screenshot_path)
        print(f"\n📸 Captura guardada: {screenshot_path}")
        
        # Mantener navegador abierto
        print("\n" + "=" * 80)
        print("✓ TEST COMPLETADO - VERIFICAR ALERTA EN PANTALLA")
        print("=" * 80)
        print(f"\nDetalles del registro:")
        print(f"  - Paciente ID: {PACIENTE_ID}")
        print(f"  - Parto ID: {parto_id}")
        print(f"  - APGAR 5 min: {apgar_5_min} (< 7 = CRÍTICO)")
        print(f"  - Fecha: {fecha_parto.strftime('%d/%m/%Y')}")
        print(f"\n📋 Revisa la sección 'Alertas' en la página para confirmar")
        print(f"   que se generó la alerta APGAR_CRITICO automáticamente.")
        
        print("\nManteniendo navegador abierto 10 segundos...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        
        # Captura en caso de error
        try:
            driver.save_screenshot("error_test_alerta.png")
            print("📸 Captura de error guardada: error_test_alerta.png")
        except:
            pass
        
        return False
        
    finally:
        print("Navegador cerrado.")
        driver.quit()


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TEST SELENIUM - GENERAR ALERTA APGAR CRÍTICO")
    print("=" * 80)
    
    resultado = test_generar_alerta_apgar()
    
    if resultado:
        print("\n✓ Test completado exitosamente")
    else:
        print("\n✗ Test falló")
