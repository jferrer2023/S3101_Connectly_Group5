from django.db import models
from django.contrib.auth.models import User

# models.py
# -------------------------------
# Defines database models for the posts app
# - Post: stores posts with type, privacy, content, author, and metadata
# - Comment: stores comments linked to posts and authors
# - Like: tracks which users liked which posts (prevents duplicates)


class Post(models.Model):
    # --- Choices for post type and privacy ---
    POST_TYPES = [
        ('text', 'Text'),
        ('video', 'Video'),
        ('image', 'Image'),
    ]

    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    # --- Fields ---
    posttype = models.CharField(
        max_length=10,
        choices=POST_TYPES,
        default='text'  # default is 'text'
    )

    title = models.CharField(
        max_length=255
   
    )

    content = models.TextField(
        default="No content",
        blank=True
    )

    privacy = models.CharField(
        max_length=10,
        choices=PRIVACY_CHOICES,
        default='public'  # default is 'public'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'   # user.posts → all posts by user
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title[:50]   # Display first 50 chars


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on '{self.post.title[:30]}'"



class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} liked '{self.post.title[:30]}'"

