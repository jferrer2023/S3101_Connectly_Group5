from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    # --- Choices ---
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
        related_name='posts'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.title[:50]


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
