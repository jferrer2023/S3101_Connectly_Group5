import sys
import os
import django

# Add project root to sys.path so Python can find posts, factories, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ---- Correct Django settings module ----
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connectly_project.settings")

# Initialize Django
django.setup()

from posts.models import Post, User
from factories.post_factory import PostFactory

# --- create a test user ---
test_user = User.objects.first()
if not test_user:
    test_user = User.objects.create(username="testuser", email="test@example.com", password="testpass")

# --- Test 1: Simple text post ---
post1 = PostFactory.create_post(
    post_type='text',
    title='Test Text Post',
    content='This is a test',
    author=test_user
)
print(f"Created post1: {post1.title}, type: {post1.posttype}, privacy: {post1.privacy}")

# --- Test 2: Image post with metadata ---
post2 = PostFactory.create_post(
    post_type='image',
    title='Test Image Post',
    content='Image content',
    metadata={'file_size': 1024},
    author=test_user
)
print(f"Created post2: {post2.title}, type: {post2.posttype}, metadata: {post2.metadata}")

# --- Test 3: Video post missing metadata (should fail) ---
try:
    post3 = PostFactory.create_post(
        post_type='video',
        title='Test Video Post',
        content='Video content',
        author=test_user
    )
except ValueError as e:
    print(f"Expected error: {e}")
