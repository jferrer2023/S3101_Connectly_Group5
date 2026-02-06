from posts.models import Post

class PostFactory:
    @staticmethod
    def create_post(post_type, title, content='', metadata=None, privacy='public', author=None):
        if metadata is None:
            metadata = {}

        if post_type not in dict(Post.POST_TYPES):
            raise ValueError("Invalid post type")

        # Metadata validation
        if post_type == 'image' and 'file_size' not in metadata:
            raise ValueError("Image posts require 'file_size' in metadata")
        if post_type == 'video' and 'duration' not in metadata:
            raise ValueError("Video posts require 'duration' in metadata")

        if author is None:
            raise ValueError("Author must be provided")

        return Post.objects.create(
            title=title,
            content=content,
            posttype=post_type,
            privacy=privacy,
            metadata=metadata,
            author=author
        )
