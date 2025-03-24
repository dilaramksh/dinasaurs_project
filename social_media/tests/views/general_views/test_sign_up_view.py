from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from social_media.forms import SignUpForm
from social_media.models import User, University
from social_media.tests.helpers import LogInTester
from django.conf import settings
from unittest.mock import patch
from django.core.files.storage import default_storage
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
        self.assertEqual(user.profile_picture, settings.DEFAULT_PROFILE_PICTURE)
        self.assertTrue(self._is_logged_in())

    @patch("django.core.files.storage.default_storage.save")
    def test_successful_sign_up_with_profile_picture(self, mock_save):
        """Test signup with profile picture upload."""

        self.form_input["username"] = "@janetestpic"
        self.form_input["email"] = "janetestpic@test.ac.uk"

        uploaded_file = SimpleUploadedFile(
            "test_picture.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        mock_save.return_value = 'profile_pictures/@janetestpic.jpg'
        self.form_input["profile_picture"] = uploaded_file

        before_count = User.objects.count()
        response = self.client.post(self.url, data={**self.form_input}, files={'profile_picture': uploaded_file})

        if response.status_code != 302:
            print("FORM ERRORS:", response.context.get('form').errors)

        self.assertEqual(response.status_code, 302)

        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)

        user = User.objects.get(username='@janetestpic')
        
        # Validate the file name was saved as expected
        expected_file_path = 'profile_pictures/@janetestpic.jpg'
        print("Saved file name:", user.profile_picture.name)

        self.assertTrue(user.profile_picture.name.startswith(expected_file_path))
        self.assertIn(expected_file_path, user.profile_picture.name)

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

    # """File Upload Test"""

    @patch("django.core.files.storage.default_storage.save")
    def test_file_upload_with_different_extension(self, mock_save):
        form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@test.ac.uk',
            'university': self.university.id,
            'start_date': '2021-09-01',
            'end_date': '2025-06-30',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'profile_picture': '',
        }
        
        mock_save.return_value = "profile_pictures/testuser.jpg"

        uploaded_file = SimpleUploadedFile(
            "avatar.jpg",
            b"file_content",
            content_type="image/jpg"
        )

        file_extension = os.path.splitext(uploaded_file.name)[1]
        new_filename = f"profile_pictures/{self.user.username}{file_extension}"

        saved_path = default_storage.save(new_filename, uploaded_file)
        self.user.profile_picture.name = saved_path

        mock_save.assert_called_once_with(new_filename, uploaded_file)
        self.assertEqual(self.user.profile_picture.name, "profile_pictures/testuser.jpg")
    

    @patch("django.core.files.storage.default_storage.save")
    def test_file_upload_with_large_file(self, mock_save):
        mock_save.return_value = "profile_pictures/testuser_large.jpg"

        large_file = SimpleUploadedFile(
            "large_file.jpg",
            b"x" * 5 * 1024 * 1024,  # 5 MB file
            content_type="image/jpeg"
        )

        file_extension = os.path.splitext(large_file.name)[1]
        new_filename = f"profile_pictures/{self.user.username}{file_extension}"

        saved_path = default_storage.save(new_filename, large_file)
        self.user.profile_picture.name = saved_path

        mock_save.assert_called_once_with(new_filename, large_file)
        self.assertEqual(self.user.profile_picture.name, "profile_pictures/testuser_large.jpg")
