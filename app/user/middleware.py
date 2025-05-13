# middleware.py

from django.http import JsonResponse
from .models import BlacklistedToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class BlacklistAccessTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Obtener el access token del encabezado Authorization
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            access_token = auth_header.split(" ")[1]

            # Verificar si el token está en la blacklist
            if BlacklistedToken.objects.filter(token=access_token).exists():
                raise InvalidToken("El token ha sido invalidado.")

        # Continuar con el procesamiento de la solicitud
        response = self.get_response(request)
        return response
