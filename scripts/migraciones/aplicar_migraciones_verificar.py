# Script de verificación para shell de Django
from apps.obstetricia.models import Parto, ComplicacionMaterna, ProtocoloVIH
from apps.neonatologia.models import RecienNacido, APGARDetalle, ComplicacionNeonatal

print("\n✅ Modelo Parto - Campos totales:", len([f for f in Parto._meta.get_fields()]))
print("✅ Modelo RecienNacido - Campos totales:", len([f for f in RecienNacido._meta.get_fields()]))
print("✅ Modelo APGARDetalle - Creado correctamente")
print("✅ Modelo ComplicacionMaterna - Creado correctamente")
print("✅ Modelo ProtocoloVIH - Creado correctamente")
print("✅ Modelo ComplicacionNeonatal - Creado correctamente\n")
