from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Logged-in user is the author
    comments = serializers.StringRelatedField(many=True, read_only=True)

    # Optional: Validate posttype and privacy using serializer fields
    posttype = serializers.ChoiceField(choices=Post.POST_TYPES, default='text')
    privacy = serializers.ChoiceField(choices=Post.PRIVACY_CHOICES, default='public')
    content = serializers.CharField(required=False, allow_blank=True, default="No content")

    class Meta:
        model = Post
        fields = ['id', 'title', 'posttype', 'privacy', 'content', 'author', 'created_at', 'metadata', 'comments']

    def create(self, validated_data):
        # Ensure author is always the logged-in user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Logged-in user is the author

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
