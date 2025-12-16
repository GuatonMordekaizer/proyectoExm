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
password = 'admin_password_123'
email = 'admin@hhm.cl'
rut = '11.111.111-1'

if not Usuario.objects.filter(username=username).exists():
    print(f"Creating user {username} with rol 'administrativo'...")
    usuario = Usuario.objects.create_superuser(
        username=username, 
        email=email, 
        password=password, 
        rut=rut,
        rol='administrativo',
        first_name='Administrador',
        last_name='Sistema'
    )
    print(f"Usuario creado exitosamente:")
    print(f"  - Rol: {usuario.rol}")
    print(f"  - Permisos: Auditoría, Gestión de Usuarios, Reportes")
else:
    print("El usuario ya existe.")
