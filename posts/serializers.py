from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment
from django.contrib.auth.models import Group

User = get_user_model()

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
            'role',          # input only
            'role_display'   # output only
        ]

    def get_role_display(self, obj):
        if obj.is_staff:
            return 'Admin'
        if obj.groups.filter(name='Moderator').exists():
            return 'Moderator'
        return 'User'

    def validate_role(self, value):
        request = self.context.get('request')

        if value and not request.user.is_staff:
            raise serializers.ValidationError(
                "Only admins can assign roles."
            )

        return value

    def create(self, validated_data):
        role = validated_data.pop('role', 'User')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)

        # Admin role
        if role == 'Admin':
            user.is_staff = True

        user.save()

        # Assign group
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.clear()
        user.groups.add(group)

        return user

    def update(self, instance, validated_data):
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

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = serializers.StringRelatedField(many=True, read_only=True)
    posttype = serializers.ChoiceField(choices=Post.POST_TYPES, default='text')
    privacy = serializers.ChoiceField(choices=Post.PRIVACY_CHOICES, default='public')
    content = serializers.CharField(required=False, allow_blank=True, default="No content")

    class Meta:
        model = Post
        fields = ['id', 'title', 'posttype', 'privacy', 'content', 'author', 'created_at', 'metadata', 'comments']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'post', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
