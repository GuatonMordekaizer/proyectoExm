from django.contrib.auth.backends import ModelBackend
from apps.administracion.models import Usuario


class RUTAuthenticationBackend(ModelBackend):
    """
    Backend de autenticación personalizado que permite login con RUT.
    Permite autenticación con RUT o username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Permite autenticación con RUT además de username.
        Verifica que la cuenta no esté bloqueada.
        """
        try:
            # Intentar buscar por RUT primero
            user = Usuario.objects.get(rut=username)
        except Usuario.DoesNotExist:
            try:
                # Si no existe por RUT, intentar por username
                user = Usuario.objects.get(username=username)
            except Usuario.DoesNotExist:
                return None
        
        # Verificar contraseña
        if user.check_password(password):
            # Verificar que la cuenta no esté bloqueada
            if user.cuenta_bloqueada or not user.activo:
                return None
            return user
        
        return None
    
    def get_user(self, user_id):
        """
        Obtiene usuario por ID.
        """
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None
