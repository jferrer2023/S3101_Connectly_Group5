from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PostViewSet, CommentViewSet, PostCommentsView, PostCommentDetailView


# posts/urls.py
# -------------------------------
# Defines all URL routes for the posts app:
# - Connects HTTP endpoints to view logic (viewsets or custom views)
# - Registers standard CRUD endpoints via DRF router for users, posts, and comments
# - Adds custom endpoints like /posts/<post_id>/comments/ for nested comments
# - Ensures each URL maps to the correct view for handling requests and responses


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
#router.register(r'comments', CommentViewSet)

urlpatterns = [
    # View all comments for a post and create a comment
    path('posts/<int:post_id>/comments/', PostCommentsView.as_view(), name='post-comments'),

    # Update / delete / get a specific comment
    path('posts/<int:post_id>/comments/<int:pk>/', PostCommentDetailView.as_view(), name='post-comment-detail'),

    # Include other routes
    path('', include(router.urls)),
]
