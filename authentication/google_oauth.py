from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
GOOGLE_CLIENT_ID = "631335029593-77gl3de0s87scfetun13db3v0oocv882.apps.googleusercontent.com"


class GoogleLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token = request.data.get("id_token")

        if not token:
            return Response(
                {"error": "ID token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify ID token with Google
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            username = email.split("@")[0]

            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": username}
            )

            if created:
                # OAuth users don't use passwords
                user.set_unusable_password()
                user.is_staff = False
                user.save()

            # Assign User group
            user_group, _ = Group.objects.get_or_create(name="User")
            user.groups.add(user_group)

            # Ensure User group has all Post & Comment permissions
            from posts.models import Post, Comment
            post_perms = Permission.objects.filter(content_type__model='post')
            comment_perms = Permission.objects.filter(content_type__model='comment')
            user_group.permissions.set(list(post_perms) + list(comment_perms))
            user_group.save()

            # Clear user's permission cache
            if hasattr(user, '_perm_cache'):
                del user._perm_cache

            # Generate JWT token
            refresh = RefreshToken.for_user(user)

            return Response({
                "message": "Google login successful",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.username,
                "email": user.email,
                "role": "User"
            })

        except ValueError:
            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )