
from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow:
    - Admins (is_staff) to access all
    - Users to access only their own objects
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.author == request.user
