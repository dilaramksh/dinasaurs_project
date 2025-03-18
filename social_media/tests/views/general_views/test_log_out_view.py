"""Tests of the log out view."""
from django.test import TestCase
from django.urls import reverse
from social_media.models import User
from social_media.tests.helpers import LogInTester

class LogOutViewTestCase(TestCase, LogInTester):
    """Tests of the log out view."""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.logout_url = reverse('log_out')
        self.homepage_url = reverse('homepage')
        self.user = User.objects.get(username='@johndoe')

    def test_log_out_url(self):
        self.assertEqual(self.logout_url,'/log_out/')

    def test_get_log_out(self):
        self.client.login(username='@johndoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.logout_url, follow=True)
        self.assertRedirects(response, self.homepage_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertFalse(self._is_logged_in())

    def test_get_log_out_without_being_logged_in(self):
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, self.homepage_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertFalse(self._is_logged_in())