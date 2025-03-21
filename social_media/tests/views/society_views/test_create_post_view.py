from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from social_media.models import User, Society, Post, University, Category
from social_media.forms import PostForm
from django.core.files.uploadedfile import SimpleUploadedFile

class CreatePostViewTests(TestCase):
    """Test cases for the create_post view."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.university = University.objects.create(name="Test University")
        self.category = Category.objects.create(name="Test Category")
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
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
        self.client.login(username='testuser', password='testpass')

    def test_create_post_view_get(self):
        """Test the create_post view with GET request."""
        response = self.client.get(reverse('create_post', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/create_post.html')
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertEqual(response.context['society'], self.society)

   
    def test_create_post_view_post_invalid(self):
        """Test the create_post view with invalid POST request."""
        post_data = {
            'title': '',  
            'content': 'This is a test post.',
        }
        response = self.client.post(reverse('create_post', args=[self.society.id]), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/create_post.html')
        self.assertIsInstance(response.context['form'], PostForm)
        self.assertIn('title', response.context['form'].errors)
        self.assertFalse(Post.objects.filter(content='This is a test post.').exists())