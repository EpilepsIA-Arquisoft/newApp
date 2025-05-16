# permissions.py
from rest_framework.permissions import BasePermission

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'doctor'

class IsBotReduce(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'reducer'

class IsBotExamenUploader(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'uploader'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'

class IsHacker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'hacker'

from rest_framework.permissions import BasePermission

class HasAnyRole(BasePermission):
    """
    Permiso base que permite el acceso solo si el rol del usuario
    está dentro de los roles permitidos.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(self, 'allowed_roles') and
            request.user.rol in self.allowed_roles
        )

def RolePermissionFactory(roles):
    """
    Devuelve una clase de permiso personalizada que autoriza
    a los usuarios que tengan uno de los roles especificados.
    """
    class CustomRolePermission(HasAnyRole):
        allowed_roles = roles

    CustomRolePermission.__name__ = f"RolePermission_{'_'.join(roles)}"
    return CustomRolePermission
