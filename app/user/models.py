from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid


class UserManager(BaseUserManager):
    def create_user(self, id, nombre, password=None, rol='doctor'):
        #if not id:
            #raise ValueError('El usuario debe tener un id')
        user = self.model(id=id, nombre=nombre, rol=rol)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, nombre, password=None):
        user = self.create_user(id=id, nombre=nombre, password=password, rol='admin')
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = (
        ('doctor', 'Doctor'),
        ('reducer', 'Reducer'),
        ('uploader', 'Uploader'),
        ('admin', 'Admin'),
    )

    id = models.CharField(primary_key=True, max_length=50, unique=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)  # El token JWT
    created_at = models.DateTimeField(auto_now_add=True)   # Cuándo fue invalidado

    def __str__(self):
        return f"Blacklisted Token {self.token[:20]}..."
