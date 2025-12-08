# Script para calcular un RUT válido con dígito verificador K

def calcular_dv(rut_sin_dv):
    """Calcula el dígito verificador de un RUT chileno"""
    suma = 0
    multiplo = 2
    
    for digito in reversed(str(rut_sin_dv)):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2
    
    resto = suma % 11
    dv_calculado = 11 - resto
    
    if dv_calculado == 11:
        return '0'
    elif dv_calculado == 10:
        return 'K'
    else:
        return str(dv_calculado)

# Buscar un RUT que tenga K como dígito verificador
print("Buscando RUTs con dígito verificador K...")
for num in range(11111111, 25000000):
    dv = calcular_dv(num)
    if dv == 'K':
        # Formatear el RUT
        rut_str = str(num)
        rut_formateado = f"{rut_str[:-6]}.{rut_str[-6:-3]}.{rut_str[-3:]}-K"
        print(f"RUT válido encontrado: {rut_formateado} (número: {num})")
        if num > 11111111:  # Encontrar algunos ejemplos
            break

# Verificar algunos RUTs específicos
ruts_a_verificar = [
    '11111111',
    '12345678',
    '24236095',
]

print("\nVerificando RUTs específicos:")
for rut in ruts_a_verificar:
    dv = calcular_dv(rut)
    rut_formateado = f"{rut[:-6]}.{rut[-6:-3]}.{rut[-3:]}-{dv}"
    print(f"RUT: {rut_formateado} (DV: {dv})")
