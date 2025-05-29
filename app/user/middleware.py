# middleware.py

from django.http import JsonResponse
from .models import BlacklistedToken, UserActivity
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from django.db import connection
from django.conf import settings
import json
import time
from django.db.utils import OperationalError

class DatabaseConnectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.retries = getattr(settings, 'DB_CONNECTION_RETRIES', 3)
        self.retry_delay = getattr(settings, 'DB_CONNECTION_RETRY_DELAY', 5)

    def __call__(self, request):
        for attempt in range(self.retries):
            try:
                # Verificar la conexión
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1")
                break
            except OperationalError:
                if attempt == self.retries - 1:
                    return JsonResponse(
                        {"detail": "Error de conexión a la base de datos"},
                        status=503
                    )
                time.sleep(self.retry_delay)
        
        response = self.get_response(request)
        return response

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

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Registrar la actividad del usuario
        if request.user.is_authenticated:
            try:
                UserActivity.objects.create(
                    user=request.user,
                    action=f"{request.method} {request.path}",
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
            except Exception:
                pass  # No queremos que un error en el logging afecte la respuesta

        response = self.get_response(request)
        
        # Agregar headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['Content-Security-Policy'] = "default-src 'self'"
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
