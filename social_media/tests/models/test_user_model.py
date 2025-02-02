from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import timedelta
from django.utils.timezone import now
from social_media.models import User

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

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_email_must_not_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.create_user(
            first_name="Jessica",
            last_name="Doe",
            email="jessica.doe@test.ac.uk",
            user_type="student",
            university=self.university,
            start_date=now().date(),
            end_date=(now() + timedelta(days=365)).date()
        )
        self.user.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user.email = 'johndoe.test.ac.uk'
        self._assert_user_is_invalid()

    def test_email_domain_must_match_university_domain(self):
        self.user.email = 'jason.doe@other.ac.uk'
        self._assert_user_is_invalid()

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
