import os
import sys
import django
from pathlib import Path

# Agregar el directorio raíz del proyecto al PYTHONPATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
django.setup()

from django.contrib.auth import get_user_model

Usuario = get_user_model()

username = 'admin_hhm'

try:
    usuario = Usuario.objects.get(username=username)
    print(f"Usuario encontrado: {usuario.username}")
    print(f"Rol actual: {usuario.rol}")
    print(f"is_superuser: {usuario.is_superuser}")
    print(f"is_staff: {usuario.is_staff}")
    
    # Actualizar rol y permisos
    usuario.rol = 'super_admin'
    usuario.is_superuser = True
    usuario.is_staff = True
    usuario.activo = True
    usuario.save()
    
    print("\n✓ Usuario actualizado correctamente:")
    print(f"  - Nuevo rol: {usuario.rol}")
    print(f"  - is_superuser: {usuario.is_superuser}")
    print(f"  - is_staff: {usuario.is_staff}")
    print(f"  - activo: {usuario.activo}")
    
except Usuario.DoesNotExist:
    print(f"El usuario '{username}' no existe.")
    print("Ejecute create_superuser.py para crearlo.")
