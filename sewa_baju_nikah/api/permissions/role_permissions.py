from rest_framework.permissions import BasePermission



# =========================================================
# IS ADMIN
# =========================================================

class IsAdminPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.profile.role == 'ADMIN'

# =========================================================
# IS KASIR
# =========================================================

class IsKasirPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.profile.role == 'KASIR'

# =========================================================
# IS USER
# =========================================================

class IsUserPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.profile.role == 'USER'

# =========================================================
# ADMIN ATAU KASIR
# =========================================================

class IsAdminOrKasirPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        return request.user.profile.role in [
            'ADMIN',
            'KASIR',
        ]