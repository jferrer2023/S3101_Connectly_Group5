from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrAdminOrModerator
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser
from singletons.logger_singleton import LoggerSingleton
from factories.post_factory import PostFactory

User = get_user_model()
logger = LoggerSingleton().get_logger()

# -------------------------------
# UserViewSet
# -------------------------------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        logger.info(f"Admin {request.user.username} accessed user list")
        return super().list(request, *args, **kwargs)

# -------------------------------
# PostViewSet
# -------------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdminOrModerator]

    def perform_create(self, serializer):
        data = serializer.validated_data
        post = PostFactory.create_post(
            post_type=data.get('posttype', 'text'),
            title=data['title'],
            content=data.get('content', ''),
            metadata=data.get('metadata', {}),
            privacy=data.get('privacy', 'public'),
            author=self.request.user
        )
        logger.info(f"User {self.request.user.username} created post '{post.title}'")


    def perform_update(self, serializer):
        serializer.save()
        logger.info(f"User {self.request.user.username} updated post '{serializer.data.get('title')}'")

    def perform_destroy(self, instance):
        logger.info(f"User {self.request.user.username} deleted post '{instance.title}'")
        instance.delete()

# -------------------------------
# CommentViewSet
# -------------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdminOrModerator]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        logger.info(
            f"User {self.request.user.username} commented on post '{serializer.validated_data['post'].title[:30]}'"
        )
