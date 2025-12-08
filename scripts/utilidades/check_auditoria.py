import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_hhm.settings')
django.setup()

from apps.administracion.models import Auditoria

try:
    total = Auditoria.objects.count()
    print(f"Total registros: {total}")
    
    if total > 0:
        print("\nPrimeros 3 registros:")
        for a in Auditoria.objects.all()[:3]:
            print(f"  - ID: {a.id}")
            print(f"    Acción: {a.accion}")
            print(f"    Usuario: {a.usuario}")
            print(f"    Timestamp: {a.timestamp}")
            print()
    else:
        print("No hay registros de auditoría")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
