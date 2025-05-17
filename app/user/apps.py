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
                {"id": "admin1", "username": "admin", "nombre": "admin", "rol": "admin", "password": "0000"},
                {"id": "doctor1", "username": "doctor1", "nombre": "doctor1", "rol": "doctor", "password": "0000"},
                {"id": "doctor2", "username": "doctor2", "nombre": "doctor2", "rol": "doctor", "password": "0000"},
                {"id": "doctor3", "username": "doctor3", "nombre": "doctor3", "rol": "doctor", "password": "0000"},
                {"id": "reducer", "username": "reducer", "nombre": "Bot Reducer", "rol": "reducer", "password": "0000"},
                {"id": "uploader", "username": "uploader", "nombre": "Bot Uploader", "rol": "uploader", "password": "0000"},
                {"id": "hacker", "username": "hacker", "nombre": "hacker", "rol": "hacker", "password": "0000"},
            ]

            for u in usuarios:
                if not User.objects.filter(id=u["id"]).exists():
                    if u["rol"] == "admin":
                        user = User.objects.create_superuser(id=u["id"], username=u["username"], nombre=u["nombre"], password=u["password"])
                    else:
                        user = User.objects.create_user(id=u["id"], username=u["username"], nombre=u["nombre"], password=u["password"], rol=u["rol"])

                else:
                    user = User.objects.get(id=u["id"])

                if u["rol"] == "doctor":
                    try:
                        from paciente.models import Paciente
                        if not Paciente.objects.filter(id="paciente1_"+u["id"]).exists():
                            Paciente.objects.create(id="paciente1_"+u["id"],nombre="Paciente1", edad=30, doctor=user)
                        if not Paciente.objects.filter(id="paciente2_"+u["id"]).exists():
                            Paciente.objects.create(id="paciente2_"+u["id"],nombre="Paciente2", edad=30, doctor=user)
                        if not Paciente.objects.filter(id="paciente3_"+u["id"]).exists():
                            Paciente.objects.create(id="paciente3_"+u["id"],nombre="Paciente3", edad=30, doctor=user)
                    except AppRegistryNotReady:
                        pass

        except OperationalError:
            pass
        except AppRegistryNotReady:
            pass
        
