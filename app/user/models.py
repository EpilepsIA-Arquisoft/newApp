from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, id, username, nombre, password=None, rol=None):
        if not username:
            raise ValueError('El usuario debe tener un username')
        if not nombre:
            raise ValueError('El usuario debe tener un nombre')
        
        user = self.model(
            id=id,
            username=username,
            nombre=nombre,
            rol=rol
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, username, nombre, password=None):
        user = self.create_user(
            id=id,
            username=username,
            nombre=nombre,
            password=password,
            rol='admin'
        )
        user.is_staff = True
        user.is_superuser = True
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
    username = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default=None)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    lockout_until = models.DateTimeField(null=True, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=32, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

    def check_login_attempts(self):
        if self.is_locked:
            if self.lockout_until and timezone.now() > self.lockout_until:
                self.is_locked = False
                self.failed_login_attempts = 0
                self.save()
                return True
            return False
        return True

    def increment_failed_login(self):
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        
        if self.failed_login_attempts >= 5:
            self.is_locked = True
            self.lockout_until = timezone.now() + timedelta(minutes=30)
        
        self.save()

    def reset_failed_login(self):
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.is_locked = False
        self.lockout_until = None
        self.save()

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted Token {self.token[:20]}..."

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "User Activities"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'session_key')
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"
