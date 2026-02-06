from factories.post_factory import PostFactory
from posts.models import Post
from django.contrib.auth.models import User
import django
import os

# Setup Django environment if running outside manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connectly_project.settings')
django.setup()

# Create a test user
user = User.objects.create_user(username='testuser', password='pass')

# Test factory
try:
    post = PostFactory.create_post(
        post_type='text',
        title='Test Factory Post',
        content='This is test content',
        metadata={},
        privacy='public',
        author=user
    )
    print(f"Post created successfully: {post.title}, ID: {post.id}")
except ValueError as e:
    print(f"Factory error: {e}")
