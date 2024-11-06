from rest_framework.permissions import BasePermission, IsAuthenticated

class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')