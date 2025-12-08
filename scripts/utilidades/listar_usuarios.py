import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
django.setup()

from apps.administracion.models import Usuario

print("=" * 80)
print("USUARIOS DEL SISTEMA")
print("=" * 80)

usuarios = Usuario.objects.all().order_by('rol', 'username')

if usuarios.exists():
    for u in usuarios:
        print(f"\n{'='*80}")
        print(f"USERNAME: {u.username}")
        print(f"RUT: {u.rut}")
        print(f"NOMBRE: {u.first_name} {u.last_name}")
        print(f"ROL: {u.get_rol_display()}")
        print(f"EMAIL: {u.email}")
        print(f"ACTIVO: {'Sí' if u.activo else 'No'}")
        print(f"SUPERUSUARIO: {'Sí' if u.is_superuser else 'No'}")
        print(f"CUENTA BLOQUEADA: {'Sí' if u.cuenta_bloqueada else 'No'}")
        print(f"INTENTOS FALLIDOS: {u.intentos_fallidos}")
        print(f"ÚLTIMO ACCESO: {u.ultimo_acceso or 'Nunca'}")
else:
    print("No hay usuarios en el sistema")

print(f"\n{'='*80}")
print(f"TOTAL: {usuarios.count()} usuarios")
print("=" * 80)

# Nota: Las contraseñas están hasheadas por seguridad
print("\nNOTA: Para probar login, usa las credenciales que conoces o crea nuevos usuarios")
print("      Las contraseñas están cifradas y no se pueden mostrar en texto plano")
