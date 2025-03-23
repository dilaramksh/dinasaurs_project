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

class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'social_media/tests/fixtures/default_user.json',
        'social_media/tests/fixtures/other_users.json'
    ]
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



    @patch('boto3.client')
    def test_profile_picture_upload(self, mock_s3_client):
        """Test successful profile picture upload."""
        self.client.login(username=self.user.username, password='Password123')
        mock_s3 = mock_s3_client.return_value

        # Simulate an image upload
        image = SimpleUploadedFile("profile.jpg", b"image data", content_type="image/jpeg")

        response = self.client.post(self.url, {'profile_picture': image}, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture, "profile_pictures/johndoe.jpg")

        # Check if S3 upload was called
        mock_s3.upload_fileobj.assert_called_once()

        messages_list = list(response.context['messages'])
        self.assertTrue(any(msg.message == "Profile updated successfully!" for msg in messages_list))

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

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture, "profile_pictures/johndoe.jpg")

        # Ensure old picture is deleted and new one is uploaded
        mock_s3.delete_object.assert_called_once_with(Bucket='your_bucket_name', Key='profile_pictures/old_picture.jpg')
        mock_s3.upload_fileobj.assert_called_once()

        messages_list = list(response.context['messages'])
        self.assertTrue(any(msg.message == "Profile updated successfully!" for msg in messages_list))

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

        # Upload a new picture
        new_image = SimpleUploadedFile("new_profile.jpg", b"new image data", content_type="image/jpeg")
        response = self.client.post(self.url, {'profile_picture': new_image}, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.profile_picture, "profile_pictures/johndoe.jpg")

        # Ensure deletion was attempted
        mock_s3.delete_object.assert_called_once()

        messages_list = list(response.context['messages'])
        self.assertTrue(any("Could not delete old profile picture" in msg.message for msg in messages_list))
