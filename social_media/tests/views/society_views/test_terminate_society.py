from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from social_media.models import Society, University, Category, User
from django.utils.timezone import now

class TerminateSocietyViewTests(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.university = University.objects.create(name="Test University")
        self.category = Category.objects.create(name="Test Category")
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass',
            email='testuser1@example.com',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
        self.society = Society.objects.create(
            name="Test Society",
            founder=self.user1,
            society_email="test@society.com",
            category=self.category
        )
        self.client.login(username='testuser1', password='testpass')

    def test_terminate_society_post(self):
        response = self.client.post(reverse('terminate_society', args=[self.society.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Society.objects.filter(id=self.society.id).exists())

    def test_terminate_society_get(self):
        response = self.client.get(reverse('terminate_society', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/terminate_society.html')