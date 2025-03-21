from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from social_media.models import University, Category, Society, Membership, Event, User
from django.utils import timezone

class HomepageViewTests(TestCase):
    """Test cases for the views in homepage_view.py."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.university = University.objects.create(
            name="Test University",
            status="approved",
            logo="university_logos/test.png"
        )

    def test_homepage_view(self):
        """Test the homepage view."""
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_discover_universities_view(self):
        """Test the discover universities view."""
        response = self.client.get(reverse('discover_universities'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/discover_universities.html')
        self.assertIn('universities', response.context)
        self.assertEqual(len(response.context['universities']), 1)

    def test_why_join_society_view(self):
        """Test the why join society view."""
        category = Category.objects.create(name="Test Category")
        society = Society.objects.create(
            name="Test Society",
            founder=User.objects.create(username='founder', password='12345', start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=365)),
            university=self.university,
            category=category,
            status="approved",
            description="Test Description",
            society_email="test@society.com",
            paid_membership=False,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational"
        )
        user = User.objects.create_user(username='testuser', password='12345', start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=365))
        Membership.objects.create(user=user, society=society)
        Event.objects.create(
            name="Test Event",
            society=society,
            date=timezone.now() + timezone.timedelta(days=1),
            location="Test Location"
        )
        response = self.client.get(reverse('why_join_society'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/why_join_society.html')
        self.assertIn('popular_societies', response.context)
        self.assertIn('upcoming_events', response.context)

    def test_latest_news_view(self):
        """Test the latest news view."""
        response = self.client.get(reverse('latest_news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/latest_news.html')

    def test_register_your_university_view_get(self):
        """Test the register your university view with GET request."""
        response = self.client.get(reverse('register_your_university'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/register_your_university.html')
        self.assertIn('form', response.context)

    def test_register_your_university_view_post_invalid(self):
        """Test the register your university view with invalid POST request."""
        post_data = {
            'name': '',
            'status': 'pending'
        }
        response = self.client.post(reverse('register_your_university'), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/register_your_university.html')
        self.assertIn('form', response.context)
        self.assertFalse(University.objects.filter(name='').exists())

    def test_register_your_university_view_post_valid(self):
        """Test the register your university view with valid POST request."""
        post_data = {
            'name': 'New University',
            'domain': 'newuniversity.edu',
        }
        response = self.client.post(reverse('register_your_university'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(University.objects.filter(name='New University').exists())

    def test_register_your_university_view_post_valid_with_file(self):
        """Test the register your university view with valid POST request including a file upload."""
        post_data = {
            'name': 'New University with Logo',
            'domain': 'newuniversitylogo.edu',
            'logo': SimpleUploadedFile("test_logo.jpg", b"file_content", content_type="image/jpeg")
        }
        response = self.client.post(reverse('register_your_university'), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))
        self.assertTrue(University.objects.filter(name='New University with Logo').exists())