from django.apps import AppConfig
from django.db.utils import OperationalError
from django.contrib.auth import get_user_model
from django.core.exceptions import AppRegistryNotReady

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        from django.db import connection
        if not connection.introspection.table_names():
            return  # evita error si las migraciones aún no se corrieron

        try:
            User = get_user_model()
            usuarios = [
                {"id": "admin", "nombre": "admin", "rol": "admin", "password": "0000"},
                {"id": "doctor", "nombre": "doctor", "rol": "doctor", "password": "0000"},
                {"id": "reducer", "nombre": "Bot Reducer", "rol": "reducer", "password": "0000"},
                {"id": "uploader", "nombre": "Bot Uploader", "rol": "uploader", "password": "0000"},
            ]

            for u in usuarios:
                if not User.objects.filter(id=u["id"]).exists():
                    if u["rol"] == "admin":
                        user = User.objects.create_superuser(id=u["id"], nombre=u["nombre"], password=u["password"])
                    else:
                        user = User.objects.create_user(id=u["id"], nombre=u["nombre"], password=u["password"], rol=u["rol"])

                else:
                    user = User.objects.get(id=u["id"])

                # Crear objeto Doctor si el usuario tiene ese rol
                if u["rol"] == "doctor":
                    try:
                        from doctor.models import Doctor
                        #if not Doctor.objects.filter(user=user).exists():
                            #Doctor.objects.create(user=user, nombre=user.nombre)
                    except AppRegistryNotReady:
                        pass

        except OperationalError:
            pass
