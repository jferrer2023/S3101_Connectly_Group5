from rest_framework import viewsets
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdmin]   

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # Without this author won't be assigned

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [DjangoModelPermissions, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # Without this author won't be assigned