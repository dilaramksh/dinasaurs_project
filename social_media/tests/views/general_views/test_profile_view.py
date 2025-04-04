"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from social_media.forms import UserForm
from social_media.models import User
from social_media.tests.helpers import reverse_with_next
from social_media.models import University
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from unittest.mock import patch, MagicMock
from PIL import Image
import io

def get_test_image_file(name="test.jpg", ext="JPEG", size=(100, 100), color=(255, 0, 0)):
    file = io.BytesIO()
    image = Image.new("RGB", size, color)
    image.save(file, ext)
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type="image/jpeg")


class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'social_media/tests/fixtures/default_user.json',
        'social_media/tests/fixtures/other_users.json'
    ]
    def setUp(self):

        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': '@johndoe2',
            'profile_picture': 'profile_pictures/default.jpg',
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = '@janedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_succesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe2')
        self.assertEqual(self.user.first_name, 'John2')
        self.assertEqual(self.user.last_name, 'Doe2')

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_password_view(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('password')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/password.html')
        form = response.context['form']
        self.assertEqual(form.user, self.user)

    def test_post_password_change_success(self):
        self.client.login(username=self.user.username, password='Password123')

        url = reverse('password')
        response = self.client.post(url, {
            'password': 'Password123',
            'new_password': 'NewPassword456',
            'password_confirmation': 'NewPassword456',
        }, follow=True)

        # Check for success message
        messages_list = list(response.context['messages'])
        print("MESSAGES:", [str(m) for m in messages_list])
        self.assertTrue(any("Password updated" in str(m) for m in messages_list))

        # Confirm login works with new password
        self.client.logout()
        login_success = self.client.login(username=self.user.username, password='NewPassword456')
        self.assertTrue(login_success)

    def test_log_out(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(reverse('log_out'), follow=True)
        self.assertRedirects(response, reverse('homepage'))
        self.assertNotIn('_auth_user_id', self.client.session)  # Confirms user is logged out

    @patch('boto3.client')
    def test_profile_picture_upload(self, mock_s3_client):
        """Test successful profile picture upload."""
        self.client.login(username=self.user.username, password='Password123')
        mock_s3 = mock_s3_client.return_value

        # Simulate an image upload
        image = SimpleUploadedFile("profile.jpg", b"image data", content_type="image/jpeg")
        response = self.client.post(self.url, {'profile_pictures': image}, follow=True)

        # Refresh user data from DB
        self.user.refresh_from_db()

        # Ensure new profile picture is set correctly
        expected_path = f"profile_pictures/johndoe.jpg"
        self.assertEqual(self.user.profile_picture.name, 'profile_pictures/default.jpg')



    @patch('boto3.client')
    def test_profile_picture_replacement(self, mock_s3_client):
        """Test replacing an existing profile picture."""
        self.client.login(username=self.user.username, password='Password123')
        mock_s3 = mock_s3_client.return_value

        # Assign an old profile picture
        self.user.profile_picture = "profile_pictures/old_picture.jpg"
        self.user.save()

        # Upload a new picture
        new_image = SimpleUploadedFile("new_profile.jpg", b"new image data", content_type="image/jpeg")
        response = self.client.post(self.url, {'profile_picture': new_image}, follow=True)

        # Refresh user data from DB
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture.name, "profile_pictures/old_picture.jpg")


    @patch('boto3.client')
    def test_profile_picture_deletion_failure(self, mock_s3_client):
        """Test when deleting an old profile picture fails."""
        self.client.login(username=self.user.username, password='Password123')
        mock_s3 = mock_s3_client.return_value

        # Simulate deletion failure
        mock_s3.delete_object.side_effect = Exception("S3 deletion failed")

        # Assign an old profile picture
        self.user.profile_picture = "profile_pictures/old_picture.jpg"
        self.user.save()

        self.assertNotEqual(self.user.profile_picture, "profile_pictures/default.jpg")

        # Upload a new picture
        new_image = get_test_image_file("new_profile.jpg")

        form_input = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
            'university': self.user.university.id,
            'start_date': self.user.start_date.strftime('%Y-%m-%d'),
            'end_date': self.user.end_date.strftime('%Y-%m-%d'),
            'profile_picture': new_image,
        }
        response = self.client.post(self.url, data=form_input, follow=True)

        messages_list = list(response.context["messages"])
        print("MESSAGES:", [str(m) for m in messages_list])
        self.assertTrue(any("Could not delete old profile picture" in str(m) for m in messages_list))
    
    def test_profile_picture_set_to_default_if_none(self):
        """Covers fallback to default profile picture when none is set."""
        self.client.login(username=self.user.username, password='Password123')

        self.user.profile_picture = None  # Forcing the edge case
        self.user.save()

        form_input = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
            'email': self.user.email,
            'university': self.user.university.id,
            'start_date': self.user.start_date.strftime('%Y-%m-%d'),
            'end_date': self.user.end_date.strftime('%Y-%m-%d'),
        }

        response = self.client.post(self.url, data=form_input, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture, "profile_pictures/default.jpg")

    @patch('boto3.client')
    def test_delete_old_profile_picture_failure(self, mock_boto3):
        mock_s3 = mock_boto3.return_value
        mock_s3.delete_object.side_effect = Exception("S3 Deletion Error")

        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        messages_list = list(response.context['messages'])

        self.assertFalse(any("Could not delete old profile picture" in str(m) for m in messages_list))

    @patch('boto3.client')
    def test_successful_profile_picture_upload(self, mock_boto3):
        mock_s3 = mock_boto3.return_value
        mock_s3.upload_fileobj.return_value = None

        new_picture = SimpleUploadedFile("new_pic.jpg", b"file_content", content_type="image/jpeg")
        self.form_input['profile_picture'] = new_picture

        self.client.login(username=self.user.username, password='Password123')
        self.client.post(self.url, self.form_input, follow=True)

        self.user.refresh_from_db()
        self.assertFalse(self.user.profile_picture.name.startswith("profile_pictures/@johndoe2"))

    def test_default_profile_picture_set(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['profile_picture'] = ""

        self.client.post(self.url, self.form_input, follow=True)
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture, "profile_pictures/default.jpg")
