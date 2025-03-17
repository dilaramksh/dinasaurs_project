from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from social_media.models import User
import hashlib

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'social_media/tests/fixtures/default_user.json',
        'social_media/tests/fixtures/other_users.json'
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user = User.objects.get(email='john.doe@test.ac.uk')

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
        self.user.profile_picture = None
        self.user.save()
        self.assertEqual(self.user.profile_picture.name, "profile_pictures/default.jpg")

    def test_profile_picture_replacement_deletes_old_picture(self):
        old_picture = SimpleUploadedFile("old_picture.jpg", b"file_content", content_type="image/jpeg")
        new_picture = SimpleUploadedFile("new_picture.jpg", b"file_content", content_type="image/jpeg")

        self.user.profile_picture = old_picture
        self.user.save()
        old_picture_path = self.user.profile_picture.name

        self.user.profile_picture = new_picture
        self.user.save()

        self.assertNotEqual(self.user.profile_picture.name, old_picture_path)

    def test_email_must_be_case_insensitive_unique(self):
        second_user = User.objects.create_user(
            first_name="Jane",
            last_name="Doe",
            email="JOHN.DOE@test.ac.uk",  # Same as existing user, but with different capitalization
            username="@janedoe",
            user_type="student",
            university=self.user.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
        self.user.email = second_user.email.lower()
        self._assert_user_is_invalid()

    def test_gravatar_hash_generation(self):
        expected_hash = hashlib.md5(self.user.email.strip().lower().encode('utf-8')).hexdigest()
        self.assertEqual(self.user.gravatar_hash, expected_hash)

    def test_start_date_cannot_be_after_end_date(self):
        self.user.start_date = now().date() + timedelta(days=365)
        self.user.end_date = now().date()
        self._assert_user_is_invalid()

    def test_default_gravatar(self):
        actual_gravatar_url = self.user.gravatar()
        expected_gravatar_url = self._gravatar_url(size=120)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_custom_gravatar(self):
        actual_gravatar_url = self.user.gravatar(size=100)
        expected_gravatar_url = self._gravatar_url(size=100)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_mini_gravatar(self):
        actual_gravatar_url = self.user.mini_gravatar()
        expected_gravatar_url = self._gravatar_url(size=60)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def _gravatar_url(self, size):
        gravatar_url = f"{UserModelTestCase.GRAVATAR_URL}?size={size}&default=mp"
        return gravatar_url

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except ValidationError:
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
