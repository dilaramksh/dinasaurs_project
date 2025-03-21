from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from social_media.models import University

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
        response = self.client.get(reverse('why_join_society'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage/why_join_society.html')

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