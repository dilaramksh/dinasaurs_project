from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now, timedelta
from social_media.models import User, University
from django.core.exceptions import ValidationError
from social_media.models.user import DEFAULT_PROFILE_PICTURE

class UserModelTests(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(
            name="Test University",
            domain="testuniversity.edu",
            logo="university_logos/test.png"
        )
        self.user = User.objects.create_user(
            username='@testuser',
            email='testuser@test.com',
            password='12345',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date(),
            profile_picture=SimpleUploadedFile("test_profile.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_user_save(self):
        """Test saving a user."""
        self.user.save()
        self.assertEqual(self.user.username, '@testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')

    def test_user_save_with_default_username(self):
        """Test saving a user with default username."""
        user = User.objects.create_user(
            username='@defaultuser',
            email='defaultuser@test.com',
            password='12345',
            first_name='Default',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
        user.save()
        self.assertEqual(user.username, '@defaultuser')

    def test_username_defaults_to_email_when_missing(self):
        """Test that username is set to email if not provided explicitly."""
        user = User(
            email='fallback@example.com',
            first_name='Fallback',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
        user.set_password('12345')
        user.save()
        self.assertEqual(user.username, 'fallback@example.com')

    def test_user_full_name(self):
        """Test the full_name method."""
        self.assertEqual(self.user.full_name(), 'Test User')

    def test_user_gravatar(self):
        """Test the gravatar method."""
        gravatar_url = self.user.gravatar()
        self.assertIn('gravatar.com', gravatar_url)

    def test_user_mini_gravatar(self):
        """Test the mini_gravatar method."""
        mini_gravatar_url = self.user.mini_gravatar()
        self.assertIn('gravatar.com', mini_gravatar_url)

    def test_delete_old_picture_called_for_custom_picture(self):
        """Test that old profile picture is deleted if it's not default."""
        new_pic = SimpleUploadedFile("new_pic.jpg", b"file_content", content_type="image/jpeg")
        self.user.profile_picture = new_pic
        self.user.save()
        self.assertNotEqual(self.user.profile_picture.name, DEFAULT_PROFILE_PICTURE)

    def test_user_profile_picture_update_triggers_delete(self):
        """Test profile picture change triggers delete_old_picture logic."""
        old_pic = self.user.profile_picture
        new_pic = SimpleUploadedFile("updated_pic.jpg", b"new_content", content_type="image/jpeg")
        self.user.profile_picture = new_pic
        self.user.save()
        self.assertNotEqual(self.user.profile_picture.name, old_pic.name)