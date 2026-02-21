from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like
from django.contrib.auth.models import Group


# serializers.py
# -------------------------------
# Defines how models (User, Post, Comment) are converted to/from JSON
# - Controls what fields are exposed in API responses
# - Handles validation, creation, and update logic
# - Adds extra computed fields (like counts, role display) for endpoints


User = get_user_model()


# UserSerializer
# Serializes user data for API
# - Controls password handling (write-only)
# - Allows admins to assign roles
# - Adds 'role_display' for readable role in API responses

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    role = serializers.ChoiceField(
        choices=['Admin', 'Moderator', 'User'],
        write_only=True,
        required=False
    )

    role_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'role',
            'role_display'
        ]

    def get_role_display(self, obj):
    # Returns readable role based on staff/group
        if obj.is_staff:
            return 'Admin'
        if obj.groups.filter(name='Moderator').exists():
            return 'Moderator'
        return 'User'

    def validate_role(self, value):
    # Only admins can assign roles
        request = self.context.get('request')

        if value and not request.user.is_staff:
            raise serializers.ValidationError(
                "Only admins can assign roles."
            )

        return value

    def create(self, validated_data):
    # Create user with password, role, and group
        role = validated_data.pop('role', 'User')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)

        if role == 'Admin':
            user.is_staff = True

        user.save()

        group, _ = Group.objects.get_or_create(name=role)
        user.groups.clear()
        user.groups.add(group)

        return user

    def update(self, instance, validated_data):
    # Update user info including password and role (admins only)
        role = validated_data.pop('role', None)
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        if role:
            if not self.context['request'].user.is_staff:
                raise serializers.ValidationError(
                    "Only admins can change roles."
                )

            instance.groups.clear()

            if role == 'Admin':
                instance.is_staff = True
            else:
                instance.is_staff = False

            group, _ = Group.objects.get_or_create(name=role)
            instance.groups.add(group)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# PostSerializer
# Serializes Post model for API
# - Read-only author fields
# - Computed fields: like_count, comment_count
# - Shows all comments via nested serializer (string representation)
# - Handles creation with current user as author

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    posttype = serializers.ChoiceField(choices=Post.POST_TYPES, default='text')
    privacy = serializers.ChoiceField(choices=Post.PRIVACY_CHOICES, default='public')
    content = serializers.CharField(required=False, allow_blank=True, default="No content")

    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    author_id = serializers.IntegerField(source='author.id', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'posttype',
            'privacy',
            'content',
            'author_id', 
            'author',
            'created_at',
            'metadata',
            'like_count',
            'comment_count',
            'comments'
        ]

    def get_like_count(self, obj): # Count of likes for this post
        return obj.likes.count()

    def get_comment_count(self, obj): # Count of comments for this post
        return obj.comments.count()

    def create(self, validated_data): # Automatically set current user as author
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)



# CommentSerializer
# Serializes Comment model for API
# - Read-only author username
# - Automatically sets current user as author on creation
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class EmptySerializer(serializers.Serializer):
    pass