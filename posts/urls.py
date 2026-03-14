from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import UserViewSet, PostViewSet, CommentViewSet, PostCommentsView, PostCommentDetailView
from .views import UserViewSet, PostViewSet, CommentViewSet, PostCommentsView, PostCommentDetailView, FeedView, UserListView

# posts/urls.py
# -------------------------------
# Defines all URL routes for the posts app:
# - Connects HTTP endpoints to view logic (viewsets or custom views)
# - Registers standard CRUD endpoints via DRF router for users, posts, and comments
# - Adds custom endpoints like /posts/<post_id>/comments/ for nested comments
# - Ensures each URL maps to the correct view for handling requests and responses


router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'posts', PostViewSet)

#router.register(r'comments', CommentViewSet)

urlpatterns = [

    #Newsfeed
    path('feed/', FeedView.as_view(), name='feed'),


    # View all comments for a post and create a comment
    path('posts/<int:post_id>/comment/', PostCommentsView.as_view(), name='post-comment'),

    # Update / delete / get a specific comment
    path('posts/<int:post_id>/comment/<int:pk>/', PostCommentDetailView.as_view(), name='post-comment-detail'),

    path('users/', UserListView.as_view(), name='user-list'),

    # Include other routes
    path('', include(router.urls)),
]