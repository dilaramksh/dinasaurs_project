from django.test import TestCase
from django.contrib.auth import get_user_model
from social_media.models import Post, Society
from django.core.exceptions import ValidationError
from datetime import date
from social_media.models.university import University

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(name="King's College London")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            start_date=date.today(), 
            end_date=date.today(),
            university = self.university
        )
        self.society = Society.objects.create(name="Test Society", description="A test society")
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user,
            society=self.society
        )

    def test_create_post(self):
        """Test if a post is correctly created."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.society, self.society)

    def test_post_str_representation(self):
        """Test the string representation of a post."""
        self.assertEqual(str(self.post), "Test Post")

    def test_post_retrieval(self):
        """Test if the post can be retrieved from the database."""
        retrieved_post = Post.objects.get(id=self.post.id)
        self.assertEqual(retrieved_post, self.post)

    def test_post_deletion(self):
        """Test if a post is successfully deleted."""
        post_id = self.post.id
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post_id)

    def test_create_post_missing_fields(self):
        """Test creating a post with missing fields."""
        with self.assertRaises(ValidationError):
            Post.objects.create(
                title="",
                content="",
                author=self.user,
                society=self.society
            )

    def test_update_post(self):
        """Test updating a post."""
        self.post.title = "Updated Test Post"
        self.post.save()
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, "Updated Test Post")

    def test_create_post_invalid_data(self):
        """Test creating a post with invalid data."""
        with self.assertRaises(ValidationError):
            Post.objects.create(
                title="Test Post",
                content="This is a test post.",
                author=None,
                society=self.society
            )