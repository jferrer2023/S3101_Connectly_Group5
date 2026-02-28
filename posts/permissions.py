from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostPermission(BasePermission): #Revised
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # READ → everyone
        if request.method in SAFE_METHODS:
            return True

        # Allow "like" action for any authenticated user
        if getattr(view, 'action', None) == 'like':
            return True

        # Admin → full access
        if user.is_staff:
            return True

        # Moderator → full access
        if user.groups.filter(name='Moderator').exists():
            return True

        # Owner → edit/delete own post
        return obj.author == user


class CommentPermission(BasePermission): #Revised
    """
    Same rules as PostPermission but for comments
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            return True

        if user.is_staff:
            return True

        if user.groups.filter(name='Moderator').exists():
            return True

        return obj.author == user