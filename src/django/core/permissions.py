# core/permissions.py
"""
Sistema de permisos personalizado para el proyecto Veterinaria.

Este archivo centraliza toda la lógica de permisos del sistema,
siguiendo las mejores prácticas de Django REST Framework.

Grupos de usuarios:
- clientes: Usuarios finales con mascotas
- veterinarios: Staff médico
- admin: Administradores (superuser)
"""

from rest_framework.permissions import BasePermission, SAFE_METHODS


# ============================================================================
# PERMISOS GENERALES POR ROL
# ============================================================================

class IsCliente(BasePermission):
    """
    Permiso: El usuario pertenece al grupo 'clientes'
    Uso: Para endpoints exclusivos de clientes
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='clientes').exists()


class IsVeterinario(BasePermission):
    """
    Permiso: El usuario pertenece al grupo 'veterinarios'
    Uso: Para endpoints exclusivos de veterinarios
    """
    def has_permission(self, request, view):
        return request.user.groups.filter(name='veterinarios').exists()


class IsVeterinarioOrAdmin(BasePermission):
    """
    Permiso: El usuario es veterinario o admin
    Uso: Para operaciones que requieren staff médico
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_staff or 
            user.groups.filter(name='veterinarios').exists()
        )


class IsAdminUser(BasePermission):
    """
    Permiso: El usuario es administrador
    Uso: Para configuraciones del sistema
    """
    def has_permission(self, request, view):
        return request.user.is_staff


class ReadOnly(BasePermission):
    """
    Permiso: Solo lectura (GET, HEAD, OPTIONS)
    Uso: Para endpoints públicos o de consulta
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


# ============================================================================
# PERMISOS ESPECÍFICOS PARA MASCOTAS
# ============================================================================

class CanManageMascota(BasePermission):
    """
    Permisos para gestionar mascotas:
    - GET: Todos (filtrado en get_queryset)
    - POST: Solo veterinarios y admins
    - PUT/PATCH/DELETE: Dueño o staff

    Uso: permission_classes = [IsAuthenticated, CanManageMascota]
    """

    def has_permission(self, request, view):
        """Validación a nivel de endpoint"""
        # GET permitido para todos (se filtra en get_queryset)
        if request.method in SAFE_METHODS:
            return True

        # POST solo para veterinarios/admins
        if request.method == 'POST':
            user = request.user
            return (
                user.is_staff or 
                user.groups.filter(name='veterinarios').exists()
            )

        # PUT/PATCH/DELETE validados en has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        """Validación a nivel de objeto (para editar/eliminar)"""
        user = request.user

        # GET permitido (ya filtrado)
        if request.method in SAFE_METHODS:
            return True

        # Veterinario/Admin puede todo
        if user.is_staff or user.groups.filter(name='veterinarios').exists():
            return True

        # Cliente solo SUS mascotas
        return obj.usuario == user


# ============================================================================
# PERMISOS ESPECÍFICOS PARA TURNOS
# ============================================================================

class CanManageTurno(BasePermission):
    """
    Permisos para gestionar turnos:
    - GET: Todos (filtrado en get_queryset)
    - POST: Todos (validación en perform_create)
    - PUT/PATCH: Solo veterinarios/admins
    - DELETE: Solo veterinarios/admins

    Uso: permission_classes = [IsAuthenticated, CanManageTurno]
    """

    def has_permission(self, request, view):
        """Validación a nivel de endpoint"""
        # GET y POST permitidos (validaciones específicas después)
        if request.method in ['GET', 'POST']:
            return True

        # PUT/PATCH/DELETE solo para veterinarios/admins
        user = request.user
        return (
            user.is_staff or 
            user.groups.filter(name='veterinarios').exists()
        )

    def has_object_permission(self, request, view, obj):
        """Validación a nivel de objeto"""
        user = request.user

        # GET permitido (ya filtrado)
        if request.method in SAFE_METHODS:
            return True

        # Veterinario/Admin puede editar/eliminar
        if user.is_staff or user.groups.filter(name='veterinarios').exists():
            return True

        # Clientes no pueden editar/eliminar (solo cancelar)
        return False


class CanCancelTurno(BasePermission):
    """
    Permiso específico para cancelar turnos:
    - Cliente: solo SUS turnos
    - Veterinario/Admin: cualquier turno

    Uso: Para el endpoint /api/turnos/{id}/cancelar/
    """

    def has_object_permission(self, request, view, obj):
        """Validar que pueda cancelar este turno"""
        user = request.user

        # Veterinario/Admin puede cancelar cualquiera
        if user.is_staff or user.groups.filter(name='veterinarios').exists():
            return True

        # Cliente solo SUS turnos
        if user.groups.filter(name='clientes').exists():
            return obj.mascota.usuario == user

        return False


# ============================================================================
# PERMISOS ESPECÍFICOS PARA ESPECIES Y RAZAS
# ============================================================================

class CanManageEspecieRaza(BasePermission):
    """
    Permisos para gestionar especies y razas:
    - GET: Todos (datos de catálogo)
    - POST/PUT/PATCH/DELETE: Solo admins

    Uso: permission_classes = [IsAuthenticated, CanManageEspecieRaza]
    """

    def has_permission(self, request, view):
        """Validación a nivel de endpoint"""
        # GET permitido para todos
        if request.method in SAFE_METHODS:
            return True

        # Modificaciones solo para admins
        return request.user.is_staff


# ============================================================================
# PERMISOS ESPECÍFICOS PARA SERVICIOS
# ============================================================================

class CanManageServicio(BasePermission):
    """
    Permisos para gestionar servicios:
    - GET: Todos (catálogo público)
    - POST/PUT/PATCH/DELETE: Solo admins

    Uso: permission_classes = [IsAuthenticated, CanManageServicio]
    """

    def has_permission(self, request, view):
        """Validación a nivel de endpoint"""
        # GET permitido para todos
        if request.method in SAFE_METHODS:
            return True

        # Modificaciones solo para admins
        return request.user.is_staff


# ============================================================================
# PERMISOS ESPECÍFICOS PARA VETERINARIOS
# ============================================================================

class CanManageVeterinarioPerfil(BasePermission):
    """
    Permisos para gestionar perfiles de veterinarios:
    - GET: Todos (para ver disponibilidad)
    - POST/PUT/PATCH/DELETE: Solo admins

    Uso: permission_classes = [IsAuthenticated, CanManageVeterinarioPerfil]
    """

    def has_permission(self, request, view):
        """Validación a nivel de endpoint"""
        # GET permitido para todos
        if request.method in SAFE_METHODS:
            return True

        # Modificaciones solo para admins
        return request.user.is_staff


# ============================================================================
# PERMISOS GENÉRICOS REUTILIZABLES
# ============================================================================

class IsOwnerOrReadOnly(BasePermission):
    """
    Permiso genérico:
    - Lectura: todos
    - Escritura: solo dueño del objeto o staff

    El objeto debe tener un campo 'usuario' que apunte al dueño.
    Uso: Para cualquier modelo que tenga relación con usuario
    """

    def has_object_permission(self, request, view, obj):
        """Validación a nivel de objeto"""
        # Lectura permitida
        if request.method in SAFE_METHODS:
            return True

        # Staff puede todo
        if request.user.is_staff:
            return True

        # Dueño puede editar
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user

        # Si no tiene campo usuario, denegar
        return False


class IsOwnerOrStaff(BasePermission):
    """
    Permiso genérico:
    - Dueño del objeto puede acceder
    - Staff puede acceder

    Similar a IsOwnerOrReadOnly pero sin restricción de método.
    Útil para endpoints donde el dueño tiene control total.
    """

    def has_object_permission(self, request, view, obj):
        """Validación a nivel de objeto"""
        user = request.user

        # Staff puede todo
        if user.is_staff or user.groups.filter(name='veterinarios').exists():
            return True

        # Validar según el tipo de objeto
        if hasattr(obj, 'usuario'):  # Mascota, etc.
            return obj.usuario == user
        elif hasattr(obj, 'mascota'):  # Turno, HistorialMedico, etc.
            return obj.mascota.usuario == user

        return False


# ============================================================================
# HELPERS
# ============================================================================

def is_cliente(user):
    """Helper para verificar si un usuario es cliente"""
    return user.groups.filter(name='clientes').exists()


def is_veterinario(user):
    """Helper para verificar si un usuario es veterinario"""
    return user.groups.filter(name='veterinarios').exists()


def is_staff_or_vet(user):
    """Helper para verificar si un usuario es staff o veterinario"""
    return user.is_staff or user.groups.filter(name='veterinarios').exists()
