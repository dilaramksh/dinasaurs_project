from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from social_media.models import User, Society, University, Category
from social_media.models.colour_history import SocietyColorHistory
from social_media.forms import CustomisationForm

class CustomiseSocietyViewTests(TestCase):
    """Test cases for the customise_society_view."""

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

    def test_customise_society_view_get(self):
        """Test the customise_society_view with GET request."""
        response = self.client.get(reverse('customise_society', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/customise_society.html')
        self.assertIsInstance(response.context['form'], CustomisationForm)
        self.assertEqual(response.context['society'], self.society)
        self.assertQuerysetEqual(response.context['past_colors'], [])

    def test_customise_society_view_post_valid(self):
        """Test the customise_society_view with valid POST request."""
        post_data = {
            'colour1': '#000000',
            'colour2': '#FFFFFF',
        }
        response = self.client.post(reverse('customise_society', args=[self.society.id]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('society_mainpage', args=[self.society.id]))
        self.society.refresh_from_db()
        self.assertEqual(self.society.colour1, '#000000')
        self.assertEqual(self.society.colour2, '#FFFFFF')
        self.assertTrue(SocietyColorHistory.objects.filter(society=self.society).exists())

    def test_customise_society_view_post_invalid(self):
        """Test the customise_society_view with invalid POST request."""
        post_data = {
            'colour1': '',  # Invalid data
            'colour2': '#FFFFFF',
        }
        response = self.client.post(reverse('customise_society', args=[self.society.id]), data=post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/customise_society.html')
        self.assertIsInstance(response.context['form'], CustomisationForm)
        self.assertIn('colour1', response.context['form'].errors)
        self.assertFalse(SocietyColorHistory.objects.filter(society=self.society).exists())


    def test_customise_society_view_post_partial_change(self):
        """Test the customise_society_view with partial change in POST request."""
        post_data = {
            'colour1': '#000000',
            'colour2': self.society.colour2,
        }
        response = self.client.post(reverse('customise_society', args=[self.society.id]), data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('society_mainpage', args=[self.society.id]))
        self.society.refresh_from_db()
        self.assertEqual(self.society.colour1, '#000000')
        self.assertEqual(self.society.colour2, '#FFF2CC')
        self.assertTrue(SocietyColorHistory.objects.filter(society=self.society).exists())