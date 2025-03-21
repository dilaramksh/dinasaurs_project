from django.test import TestCase
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from social_media.models import Post, Society, Category, User, University

class PostModelTest(TestCase):
    """Test cases for the Post model."""

    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(name="Test University")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            user_type="student",
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
        self.category = Category.objects.create(name="Test Category")
        self.society = Society.objects.create(
            name="Test Society",
            founder=self.user,
            society_email="test@society.com",
            description="A test society",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.post = Post.objects.create(
            title="Test Post",
            content="This is a test post.",
            author=self.user,
            society=self.society,
            picture="post_pictures/default.jpg"
        )

    def test_post_creation(self):
        """Test if a Post instance is correctly created."""
        self.assertEqual(self.post.title, "Test Post")
        self.assertEqual(self.post.content, "This is a test post.")
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.society, self.society)
        self.assertEqual(self.post.picture, "post_pictures/default.jpg")
        self.assertIsNotNone(self.post.created_at)

    def test_post_str_representation(self):
        """Test the string representation of a Post instance."""
        self.assertEqual(str(self.post), "Test Post")

    def test_post_retrieval(self):
        """Test if the Post instance can be retrieved from the database."""
        retrieved_post = Post.objects.get(id=self.post.id)
        self.assertEqual(retrieved_post, self.post)

    def test_post_deletion(self):
        """Test if a Post instance is successfully deleted."""
        post_id = self.post.id
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=post_id)

    def test_post_update(self):
        """Test if a Post instance is successfully updated."""
        self.post.title = "Updated Test Post"
        self.post.save()
        updated_post = Post.objects.get(id=self.post.id)
        self.assertEqual(updated_post.title, "Updated Test Post")