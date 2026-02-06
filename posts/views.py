from rest_framework import viewsets
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from singletons.logger_singleton import LoggerSingleton

# -------------------------------
# Logger setup (singleton)
# -------------------------------
# Using LoggerSingleton ensures that the same logger instance
# is used throughout the project. All logs go to the same file/format.
logger = LoggerSingleton().get_logger()


# -------------------------------
# UserViewSet
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admins can access users

    def list(self, request, *args, **kwargs):
        # Log when an admin fetches the user list
        logger.info(f"Admin {request.user.username} accessed user list")
        return super().list(request, *args, **kwargs)


# -------------------------------
# PostViewSet
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Assign logged-in user as author
        serializer.save(author=self.request.user)
        # Log post creation with title
        logger.info(f"User {self.request.user.username} created a new post '{serializer.data.get('title')}'")

    def perform_update(self, serializer):
        # Save updates
        serializer.save()
        # Log post update with title
        logger.info(f"User {self.request.user.username} updated post '{serializer.data.get('title')}'")

    def perform_destroy(self, instance):
        # Log deletion before removing from DB
        logger.info(f"User {self.request.user.username} deleted post '{instance.title}'")
        instance.delete()


# -------------------------------
# CommentViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Assign logged-in user as author
        serializer.save(author=self.request.user)
        # Log comment creation with post title snippet
        logger.info(
            f"User {self.request.user.username} commented on post "
            f"'{serializer.validated_data['post'].title[:30]}'"
        )
