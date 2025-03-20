from django.test import TestCase
from social_media.forms import EventCreationForm
from social_media.models import Event
from datetime import date

class EventCreationFormTest(TestCase):
    """Test cases for the EventCreationForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date': date.today(),
            'location': 'Test Location',
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with invalid data."""
        form_data = {
            'name': '',
            'description': 'This is a test event.',
            'date': 'invalid-date',
            'location': 'Test Location',
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('date', form.errors)

    def test_form_missing_data(self):
        """Test form with missing data."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('location', form.errors)

    def test_form_empty_data(self):
        """Test form with empty data."""
        form_data = {}
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('location', form.errors)

    def test_form_optional_picture(self):
        """Test form with optional picture field."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date': date.today(),
            'location': 'Test Location',
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('picture', form.errors)