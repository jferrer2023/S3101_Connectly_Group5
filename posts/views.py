from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, EmptySerializer
from .permissions import PostPermission, CommentPermission
from rest_framework.permissions import DjangoModelPermissions, IsAdminUser, IsAuthenticated
from rest_framework.generics import ListAPIView
from singletons.logger_singleton import LoggerSingleton
from factories.post_factory import PostFactory
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.views import APIView
from django.db.models import Q



# views.py
# -------------------------------
# Handles the logic for API endpoints:
# - Connects models (Post, Comment, User) to serializers
# - Manages CRUD operations for posts, comments, and users
# - Adds extra actions like comments dropdown and like/unlike
# - Controls permissions and pagination
# - Logs user actions for tracking



User = get_user_model()
logger = LoggerSingleton().get_logger()

# User management for admin only (CRUD users)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        logger.info(f"Admin {request.user.username} accessed user list")
        return super().list(request, *args, **kwargs)


# Posts CRUD + like/unlike + get comments
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostPermission] #Revised

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.groups.filter(name='Moderator').exists():
            return Post.objects.all().order_by('-created_at')

        return Post.objects.filter(
            Q(privacy='public') | Q(author=user)
        ).order_by('-created_at')
    
    # Corrected perform_create
    def perform_create(self, serializer):
        # Save serializer → returns a Post model instance
        post = serializer.save(author=self.request.user)

        # Log creation
        logger.info(f"User {self.request.user.username} created post '{post.title}'")

    def perform_update(self, serializer):
        post = serializer.save()
        logger.info(f"User {self.request.user.username} updated post '{post.title}'")

    def perform_destroy(self, instance):
        logger.info(f"User {self.request.user.username} deleted post '{instance.title}'")
        instance.delete()

    # Comment dropdown Extra Action
    # GET /posts/<id>/comments/ → list all comments for this post
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # POST /posts/<id>/like/ → like/unlike post
    @action(detail=True, methods=['post'], serializer_class=EmptySerializer)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            like.delete()
            return Response({"message": "Post unliked"}, status=status.HTTP_200_OK)

        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)



# Comments CRUD
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission] #Revised

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        logger.info(
            f"User {self.request.user.username} commented on post '{comment.post.title[:30]}'"
        )


# Pagination for comments
class CommentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'limit'
    max_page_size = 50


# Comments CRUD
class PostCommentsView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission] #Revised
    pagination_class = CommentPagination

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(author=self.request.user, post_id=post_id)

# Retrieve / update / delete a specific comment under a post
class PostCommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission] #Revised
    

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)

# Newsfeed
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(
            Q(privacy='public') | Q(author=user)
        ).select_related('author').prefetch_related('comments', 'likes').order_by('-created_at')
        return queryset

    def list(self, request, *args, **kwargs):
        user = request.user
        page = request.query_params.get('page', 1)
        cache_key = f'feed_user_{user.id}_page_{page}'
        cached_data = cache.get(cache_key)

        if cached_data:
            logger.info(f"CACHE HIT ✅ for user {user.username} page {page}")
            response = Response(cached_data)
            response["X-Cache"] = "HIT"
        else:
            logger.info(f"CACHE MISS ❌ for user {user.username} page {page}")
            queryset = self.get_queryset()
            page_obj = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page_obj, many=True)
            response_data = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, response_data, timeout=30)
            response = Response(response_data)
            response["X-Cache"] = "MISS"

        # Add request logging in the desired format
        logger.info(f"INFO - {request.method} {request.path} - status={response.status_code}")

        return response


User = get_user_model()

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]