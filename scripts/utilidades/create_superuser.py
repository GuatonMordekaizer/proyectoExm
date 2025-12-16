import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
django.setup()

Usuario = get_user_model()

username = 'admin_hhm'
password = 'admin_password_123'
email = 'admin@hhm.cl'
rut = '11.111.111-1'

if not Usuario.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    Usuario.objects.create_superuser(username=username, email=email, password=password, rut=rut, rol='super_admin')
    print("Superuser created.")
else:
    print("Superuser already exists.")
