from django.test import TestCase, Client
from django.urls import reverse

class FooterViewTests(TestCase):
    """Test cases for the views in footer_view.py."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()


    def test_contact_us_view(self):
        """Test the contact us view."""
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/footer/contact_us.html')

    def test_privacy_policy_view(self):
        """Test the privacy policy view."""
        response = self.client.get(reverse('privacy_policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'partials/footer/privacy_policy.html')