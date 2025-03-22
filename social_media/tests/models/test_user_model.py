from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from unittest.mock import patch
from django.test import TestCase
from django.utils.timezone import now

from social_media.models import User, University
from django.utils.timezone import now, timedelta
from social_media.models import User, University
from django.core.exceptions import ValidationError
from social_media.models.user import DEFAULT_PROFILE_PICTURE
import hashlib

class UserModelTests(TestCase):
    """Test cases for the User model."""

    def setUp(self):
        self.university = University.objects.create(
            name="Test University",
            domain='test.ac.uk',
        )

        self.user = User.objects.create_user(
            username="@testuser",
            password="testpass",
            email="testuser@test.ac.uk",
            first_name="Test",
            last_name="User",
            user_type="student",
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
        )

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'invalidUsername'
        self._assert_user_is_invalid()

    def test_username_must_have_at_least_four_characters(self):
        self.user.username = '@ab'
        self._assert_user_is_invalid()

    def test_username_may_contain_letters_numbers_and_underscores(self):
        self.user.username = '@valid_123'
        self._assert_user_is_valid()

    def test_profile_picture_defaults_if_not_provided(self):
        user2 = User.objects.create(
            first_name='Jana',
            last_name='Doee',
            email='janedoee@test.ac.uk',
            user_type='student',
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janey',
        )
        self.assertEqual(user2.profile_picture.name, "profile_pictures/default.jpg")


    def test_email_must_be_case_insensitive_unique(self):
        second_user = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="JOHN.DOE@test.ac.uk",  # Same as existing user, but with different capitalization
            username="@janedoe",
            user_type="student",
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
        )
        second_user.email = second_user.email.lower()
        self.assertEqual(second_user.email, "john.doe@test.ac.uk")
   

    def test_start_date_cannot_be_after_end_date(self):
        third_user = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="JOHN.DOE@test.ac.uk",
            username="@janedoe",
            user_type="student",
            university=self.university,
            start_date='2023-09-23',
            end_date='2021-05-06',
        )
        self.assertGreaterEqual(third_user.start_date, third_user.end_date)
    
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    @patch.object(default_storage, 'delete')
    def test_delete_old_picture(self, mock_delete):
        """Ensure old profile pictures are deleted from S3 when updated"""

        fourth_test = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="test4@test.ac.uk",
            username="@test4",
            user_type="student",
            university=self.university,
            start_date='2023-09-23',
            end_date='2021-05-06',
            profile_picture=SimpleUploadedFile(name="old_pic.jpg", content=b"old_picture", content_type="image/jpeg")
        )

        new_picture = SimpleUploadedFile(name="new_pic.jpg", content=b"new_picture", content_type="image/jpeg")
        fourth_test.profile_picture = new_picture
        fourth_test.save()

        mock_delete.assert_called_with("profile_pictures/old_pic.jpg")
