from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_media.models import Society, Membership, Event

User = get_user_model()

class TerminateSocietyViewTest(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpass")

        self.society = Society.objects.create(name="Test Society", description="A test society")
        
        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        
        session = self.client.session
        session['active_society_id'] = self.society.id
        session.save()

        self.url = reverse('terminate_society', args=[self.society.id])

    def test_non_admin_cannot_terminate_society(self):
        """Test that a non-admin user cannot terminate the society."""
        self.client.logout()
        self.client.login(username="otheruser", password="otherpass")

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)  # Assuming a 403 Forbidden response

        self.assertTrue(Society.objects.filter(id=self.society.id).exists())

    def test_terminate_society_already_deleted(self):
        """Test behavior when trying to delete a society that was already deleted."""
        self.society.delete()
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_get_terminate_society_page_renders_correctly(self):
        """Ensure the GET request properly renders the termination page."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/terminate_society.html')
        self.assertContains(response, self.society.name)

    def test_session_clearing_when_no_active_society(self):
        """Ensure the session key removal does not raise errors when missing."""
        session = self.client.session
        del session['active_society_id']
        session.save()

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("dashboard"))
