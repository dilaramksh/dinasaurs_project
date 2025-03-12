from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from social_media.forms import SignUpForm
from social_media.models import User, University
from social_media.tests.helpers import LogInTester
from django.conf import settings
import os

class SignUpViewTestCase(TestCase, LogInTester):
    """Tests of the sign up view."""

    def setUp(self):
        self.url = reverse('sign_up')
        self.university = University.objects.create(name="Test University", domain="test.ac.uk", status="approved")
        
        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@test.ac.uk',
            'university': self.university.id,
            'start_date': '2021-09-01',
            'end_date': '2025-06-30',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
        }
        
        self.profile_picture = SimpleUploadedFile(
            "profile.jpg", b"profile_picture_content", content_type="image/jpeg"
        )
        
    
        self.user = User.objects.create_user(
            username='@johndoe',
            email='johndoe@test.ac.uk',
            university=self.university,
            start_date='2023-09-15',
            end_date='2026-06-15',
            password='Password123',
        )
        

    def test_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/')

    def test_get_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/sign_up.html')
        form = response.context['form']
        self.assertIsInstance(form, SignUpForm)
        self.assertFalse(form.is_bound)

    def test_redirect_if_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))

    def test_unsuccessful_sign_up(self):
        self.form_input['username'] = 'bad_username'  # Assuming it fails validation
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/sign_up.html')
        self.assertFalse(self._is_logged_in())

    def test_successful_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@test.ac.uk')
        self.assertTrue(check_password('Password123', user.password))
        self.assertTrue(self._is_logged_in())

    def test_successful_sign_up_with_profile_picture(self):
        self.form_input['profile_picture'] = self.profile_picture
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username='@janedoe')
        self.assertTrue(user.profile_picture.name.startswith('profile_pictures/@janedoe'))
        self.assertTrue(os.path.exists(user.profile_picture.path))

    def test_default_profile_picture_if_none_uploaded(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.profile_picture, settings.DEFAULT_PROFILE_PICTURE)

    def test_redirect_after_sign_up(self):
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))
        self.assertTrue(self._is_logged_in())

    def test_post_sign_up_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count) 
        self.assertRedirects(response, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))


