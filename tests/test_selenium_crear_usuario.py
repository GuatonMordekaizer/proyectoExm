"""
Test de Selenium para automatizar la creación de usuarios.
Prueba el formulario completo de registro de usuario Médico Gineco-Obstetra.
"""

import time
from datetime import date
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


def test_crear_usuario_medico():
    """
    Test completo de creación de usuario Médico Gineco-Obstetra.
    Completa todos los campos del formulario y verifica el registro exitoso.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("=" * 80)
        print("TEST: CREAR USUARIO MÉDICO GINECO-OBSTETRA")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN COMO ADMINISTRADOR O JEFE DE SERVICIO
        # ===================================================================
        print("\n[1/4] Iniciando sesión como jefe de servicio...")
        driver.get("http://127.0.0.1:8000/auth/login/")
        
        # Login como jefe de servicio (tiene permisos para crear usuarios)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin_hhm")  # Usuario jefe de servicio
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("admin_password_123")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Esperar que cargue el dashboard
        time.sleep(2)
        current_url = driver.current_url
        
        if "/auth/login/" in current_url:
            print("✗ ERROR: No se pudo iniciar sesión con las credenciales proporcionadas")
            print("  Intenta con otro usuario con permisos administrativos")
            return False
        
        print("✓ Sesión iniciada correctamente")
        
        # ===================================================================
        # PASO 2: NAVEGAR AL FORMULARIO DE CREAR USUARIO
        # ===================================================================
        print("\n[2/4] Navegando al formulario de crear usuario...")
        driver.get("http://127.0.0.1:8000/auth/usuarios/crear/")
        
        # Esperar que cargue el formulario
        time.sleep(2)
        
        # Verificar que estamos en el formulario
        current_url = driver.current_url
        if "/auth/login/" in current_url:
            print("✗ ERROR: Usuario no tiene permisos para crear usuarios")
            return False
        
        if "/usuarios/crear/" not in current_url:
            print(f"✗ ERROR: No se pudo acceder al formulario. URL actual: {current_url}")
            return False
        
        print("✓ Formulario de crear usuario cargado")
        
        # ===================================================================
        # PASO 3: COMPLETAR FORMULARIO
        # ===================================================================
        print("\n[3/4] Completando formulario de usuario...")
        
        # Generar datos de prueba
        rut_usuario = generar_rut_valido()
        username_nuevo = f"medico_{rut_usuario[:8].replace('.', '')}"  # medico_12345678
        
        print(f"\nDatos del usuario a crear:")
        print(f"  RUT: {rut_usuario}")
        print(f"  Username: {username_nuevo}")
        print(f"  Nombre: Dr. Juan Carlos")
        print(f"  Apellido: Fernández López")
        print(f"  Email: {username_nuevo}@hospital.cl")
        print(f"  Rol: Médico Gineco-Obstetra")
        
        # --- USERNAME ---
        username_input = driver.find_element(By.ID, "id_username")
        username_input.clear()
        username_input.send_keys(username_nuevo)
        print("\n  ✓ Username completado")
        
        # --- RUT ---
        rut_input = driver.find_element(By.ID, "id_rut")
        rut_input.clear()
        rut_input.send_keys(rut_usuario)
        print("  ✓ RUT completado")
        
        # --- NOMBRE ---
        first_name_input = driver.find_element(By.ID, "id_first_name")
        first_name_input.clear()
        first_name_input.send_keys("Juan Carlos")
        print("  ✓ Nombre completado")
        
        # --- APELLIDO ---
        last_name_input = driver.find_element(By.ID, "id_last_name")
        last_name_input.clear()
        last_name_input.send_keys("Fernández López")
        print("  ✓ Apellido completado")
        
        # --- EMAIL ---
        email_input = driver.find_element(By.ID, "id_email")
        email_input.clear()
        email_input.send_keys(f"{username_nuevo}@hospital.cl")
        print("  ✓ Email completado")
        
        # --- ROL ---
        rol_select = Select(driver.find_element(By.ID, "id_rol"))
        rol_select.select_by_value("medico_obstetra")
        print("  ✓ Rol 'Médico Gineco-Obstetra' seleccionado")
        
        # --- CONTRASEÑA (si el formulario la pide en creación) ---
        try:
            password1_input = driver.find_element(By.ID, "id_password1")
            password1_input.clear()
            password1_input.send_keys("TempPass@2024")
            
            password2_input = driver.find_element(By.ID, "id_password2")
            password2_input.clear()
            password2_input.send_keys("TempPass@2024")
            print("  ✓ Contraseñas completadas")
        except NoSuchElementException:
            print("  ⚠ Campos de contraseña no encontrados (puede ser normal)")
        
        time.sleep(1)
        
        # ===================================================================
        # PASO 4: ENVIAR FORMULARIO
        # ===================================================================
        print("\n[4/4] Enviando formulario...")
        
        # Verificar URL antes de enviar
        current_url_before = driver.current_url
        print(f"  URL antes de enviar: {current_url_before}")
        
        # Buscar el botón submit
        # Buscar el botón CORRECTO (el primario del formulario, no el de logout)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(0.5)
        
        # Verificar token CSRF
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
        
        # Enviar formulario usando JavaScript
        driver.execute_script("arguments[0].click();", submit_button)
        print("✓ Formulario enviado")
        
        # ===================================================================
        # PASO 5: VERIFICAR RESULTADO
        # ===================================================================
        print("\n[5/5] Verificando resultado...")
        time.sleep(3)
        
        # Verificar URL actual
        current_url = driver.current_url
        print(f"  URL después de enviar: {current_url}")
        
        # Buscar errores
        try:
            error_alert = driver.find_element(By.CSS_SELECTOR, ".alert-danger")
            print("✗ ERROR: Se encontraron errores en el formulario")
            print(f"  Mensaje: {error_alert.text}")
            
            # Buscar errores específicos
            field_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger")
            if field_errors:
                print("\n  Errores de campos:")
                for error in field_errors:
                    if error.text.strip():
                        print(f"    - {error.text}")
            
            time.sleep(10)
            return False
            
        except NoSuchElementException:
            print("✓ No se encontraron errores en el formulario")
        
        # Verificar redirección exitosa
        if "/usuarios/" in current_url and "/usuarios/crear/" not in current_url:
            print("✓ Redirección exitosa después de crear usuario")
            
            # Buscar mensaje de éxito
            try:
                success_message = driver.find_element(By.CSS_SELECTOR, ".alert-success, .alert-info")
                print(f"✓ Mensaje de éxito: {success_message.text}")
            except NoSuchElementException:
                print("  (No se encontró mensaje de éxito explícito, pero hubo redirección)")
            
            print("\n" + "=" * 80)
            print("✓ TEST EXITOSO: USUARIO MÉDICO CREADO CORRECTAMENTE")
            print("=" * 80)
            print(f"\nUsuario creado:")
            print(f"  - RUT: {rut_usuario}")
            print(f"  - Username: {username_nuevo}")
            print(f"  - Nombre: Dr. Juan Carlos Fernández López")
            print(f"  - Email: {username_nuevo}@hospital.cl")
            print(f"  - Rol: Médico Gineco-Obstetra")
            
            return True
            
        else:
            print(f"⚠ ADVERTENCIA: URL inesperada después de enviar: {current_url}")
            print("  Se esperaba redirección a lista de usuarios")
            
            # Verificar si seguimos en el formulario
            if "/usuarios/crear/" in current_url:
                print("  ⚠ Seguimos en el formulario de creación")
                print("  Buscando errores no detectados...")
                
                all_errors = driver.find_elements(By.CSS_SELECTOR, ".text-danger, .alert-danger")
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
        print("\nManteniendo navegador abierto 5 segundos...")
        time.sleep(5)
        driver.quit()
        print("Navegador cerrado.")


if __name__ == "__main__":
    print("\n" + "╔" + "=" * 78 + "╗")
    print("║" + " " * 18 + "TEST SELENIUM - CREAR USUARIO MÉDICO" + " " * 24 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\nEste test automatiza el formulario de creación de usuario Médico Gineco-Obstetra.")
    print("Requisito: El servidor debe estar corriendo en http://127.0.0.1:8000")
    print("Requisito: Usa el usuario admin_hhm (jefe de servicio) para crear el usuario")
    print("\nPresione Ctrl+C para cancelar...\n")
    
    try:
        time.sleep(2)
        resultado = test_crear_usuario_medico()
        
        if resultado:
            print("\n✓ Test completado exitosamente")
            exit(0)
        else:
            print("\n✗ Test falló")
            exit(1)
            
    except KeyboardInterrupt:
        print("\n\nTest cancelado por el usuario")
        exit(1)
