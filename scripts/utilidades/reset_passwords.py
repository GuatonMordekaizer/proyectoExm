import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
django.setup()

from apps.administracion.models import Usuario

print("=" * 80)
print("ESTABLECIENDO CONTRASEÑAS PARA USUARIOS DE PRUEBA")
print("=" * 80)

# Contraseña común para todos los usuarios demo
PASSWORD = "hospital2025"

usuarios_actualizar = [
    {'username': 'admin_hhm', 'password': 'admin_password_123'},
    {'username': 'matrona_demo', 'password': PASSWORD},
]

for data in usuarios_actualizar:
    try:
        usuario = Usuario.objects.get(username=data['username'])
        usuario.set_password(data['password'])
        usuario.save()
        print(f"✓ Contraseña actualizada para: {usuario.username} ({usuario.get_rol_display()})")
        print(f"  Usuario: {usuario.username}")
        print(f"  RUT: {usuario.rut}")
        print(f"  Contraseña: {data['password']}")
        print()
    except Usuario.DoesNotExist:
        print(f"✗ Usuario {data['username']} no existe")
        print()

print("=" * 80)
print("RESUMEN DE CREDENCIALES")
print("=" * 80)
print("\n1. Jefe de Servicio:")
print("   Usuario: admin_hhm")
print("   Contraseña: admin_password_123")
print("   RUT: 11.111.111-1")
print("\n2. Matrona Demo:")
print("   Usuario: matrona_demo")
print("   Contraseña: hospital2025")
print("   RUT: 12.345.678-5")
print("\n" + "=" * 80)
