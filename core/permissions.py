from rest_framework import permissions



class IsAdminOrIsAuthenticated(permissions.BasePermission):
    """
    The request is admin as a user, or is a authenticated user.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS :
            return bool(request.user and request.user.is_staff)
        return bool(
            request.user and
            request.user.is_authenticated
        )