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


def crear_usuario(driver, wait, username, rut, nombre, apellido, email, password="doc@12345678"):
    """
    Función auxiliar para crear un usuario médico.
    """
    print(f"\n  Creando usuario: {username}")
    
    # Navegar al formulario
    driver.get("http://127.0.0.1:8000/auth/usuarios/crear/")
    time.sleep(2)
    
    # Verificar acceso
    if "/auth/login/" in driver.current_url:
        print("    ✗ Usuario no tiene permisos")
        return False
    
    # Completar formulario
    driver.find_element(By.ID, "id_username").clear()
    driver.find_element(By.ID, "id_username").send_keys(username)
    
    driver.find_element(By.ID, "id_rut").clear()
    driver.find_element(By.ID, "id_rut").send_keys(rut)
    
    driver.find_element(By.ID, "id_first_name").clear()
    driver.find_element(By.ID, "id_first_name").send_keys(nombre)
    
    driver.find_element(By.ID, "id_last_name").clear()
    driver.find_element(By.ID, "id_last_name").send_keys(apellido)
    
    driver.find_element(By.ID, "id_email").clear()
    driver.find_element(By.ID, "id_email").send_keys(email)
    
    rol_select = Select(driver.find_element(By.ID, "id_rol"))
    rol_select.select_by_value("medico_obstetra")
    
    # Contraseñas si existen
    try:
        driver.find_element(By.ID, "id_password1").clear()
        driver.find_element(By.ID, "id_password1").send_keys(password)
        driver.find_element(By.ID, "id_password2").clear()
        driver.find_element(By.ID, "id_password2").send_keys(password)
    except NoSuchElementException:
        pass
    
    time.sleep(1)
    
    # Enviar
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit'].btn-primary")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", submit_button)
    time.sleep(3)
    
    # Verificar resultado
    current_url = driver.current_url
    if "/usuarios/" in current_url and "/usuarios/crear/" not in current_url:
        print(f"    ✓ Usuario {username} creado exitosamente")
        return True
    else:
        print(f"    ✗ Error al crear usuario {username}")
        return False


def test_crear_usuario_medico():
    """
    Test de creación de 2 usuarios Médico Gineco-Obstetra.
    Crea: medico_g (usado por otros tests) + un usuario aleatorio.
    """
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    try:
        print("=" * 80)
        print("TEST: CREAR 2 USUARIOS MÉDICO GINECO-OBSTETRA")
        print("=" * 80)
        
        # ===================================================================
        # PASO 1: LOGIN COMO ADMINISTRADOR
        # ===================================================================
        print("\n[1/3] Iniciando sesión como jefe de servicio...")
        driver.get("http://127.0.0.1:8000/auth/login/")
        
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        username_input.send_keys("admin_hhm")
        
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys("admin_password_123")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        time.sleep(2)
        
        if "/auth/login/" in driver.current_url:
            print("✗ ERROR: No se pudo iniciar sesión")
            return False
        
        print("✓ Sesión iniciada correctamente")
        
        # ===================================================================
        # PASO 2: CREAR USUARIO 1 - medico_g (PARA OTROS TESTS)
        # ===================================================================
        print("\n[2/3] Creando usuario principal para tests: medico_g")
        print("  RUT: 20.364.050-1")
        print("  Username: medico_g")
        print("  Password: doc@12345678")
        print("  Rol: Médico Gineco-Obstetra")
        
        resultado1 = crear_usuario(
            driver, wait,
            username="medico_g",
            rut="20.364.050-1",
            nombre="Dr. Gineco",
            apellido="Obstetra",
            email="medico_g@hospital.cl",
            password="doc@12345678"
        )
        
        if not resultado1:
            print("\n⚠ ADVERTENCIA: No se pudo crear medico_g (puede que ya exista)")
        
        # ===================================================================
        # PASO 3: CREAR USUARIO 2 - USUARIO ALEATORIO
        # ===================================================================
        print("\n[3/3] Creando segundo usuario médico...")
        
        rut_aleatorio = generar_rut_valido()
        username_aleatorio = f"medico_{rut_aleatorio[:8].replace('.', '')}"
        
        print(f"  RUT: {rut_aleatorio}")
        print(f"  Username: {username_aleatorio}")
        print(f"  Password: TempPass@2024")
        print(f"  Rol: Médico Gineco-Obstetra")
        
        resultado2 = crear_usuario(
            driver, wait,
            username=username_aleatorio,
            rut=rut_aleatorio,
            nombre="Juan Carlos",
            apellido="Fernández López",
            email=f"{username_aleatorio}@hospital.cl",
            password="TempPass@2024"
        )
        
        # ===================================================================
        # PASO 4: RESUMEN
        # ===================================================================
        print("\n" + "=" * 80)
        print("RESUMEN DE CREACIÓN DE USUARIOS")
        print("=" * 80)
        
        if resultado1:
            print("✓ Usuario 1: medico_g creado exitosamente")
            print("  → Este usuario es usado por test_selenium_registrar_parto.py")
            print("  → Este usuario es usado por test_selenium_generar_alerta.py")
        else:
            print("⚠ Usuario 1: medico_g no se pudo crear (puede existir)")
        
        if resultado2:
            print(f"✓ Usuario 2: {username_aleatorio} creado exitosamente")
        else:
            print(f"✗ Usuario 2: {username_aleatorio} falló")
        
        if resultado1 or resultado2:
            print("\n✓ TEST COMPLETADO: Al menos 1 usuario fue creado")
            return True
        else:
            print("\n✗ TEST FALLÓ: Ningún usuario pudo ser creado")
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
    print("║" + " " * 15 + "TEST SELENIUM - CREAR 2 USUARIOS MÉDICOS" + " " * 22 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\nEste test crea 2 usuarios Médico Gineco-Obstetra:")
    print("  1. medico_g (usado por otros tests de Selenium)")
    print("  2. Usuario aleatorio adicional")
    print("\nRequisito: El servidor debe estar corriendo en http://127.0.0.1:8000")
    print("Requisito: Usa el usuario admin_hhm (jefe de servicio) para crear usuarios")
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
