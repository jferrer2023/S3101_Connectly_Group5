
from rest_framework.permissions import BasePermission

class IsOwnerOrAdminOrModerator(BasePermission):
    """
    Admins can do anything.
    Moderators can view, edit, delete posts.
    Users can only access their own posts.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admins
        if user.is_staff:
            return True
        
        # Moderators
        if user.groups.filter(name='Moderator').exists():
            return True
        
        # Regular users can access only their own posts
        return obj.author == user
