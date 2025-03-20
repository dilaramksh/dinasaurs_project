from django.test import TestCase
from social_media.forms import PostForm
from social_media.models import Post

class PostFormTest(TestCase):
    """Test cases for the PostForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with invalid data."""
        form_data = {
            'title': '',
            'content': 'This is a test post.',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_form_missing_data(self):
        """Test form with missing data."""
        form_data = {
            'title': 'Test Post',
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)

    def test_form_empty_data(self):
        """Test form with empty data."""
        form_data = {}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('content', form.errors)

    def test_form_optional_picture(self):
        """Test form with optional picture field."""
        form_data = {
            'title': 'Test Post',
            'content': 'This is a test post.',
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('picture', form.errors)