from django.test import TestCase
from social_media.forms import EventCreationForm
from social_media.models import Event
from datetime import date
from datetime import timedelta

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

    def test_form_date_in_the_past(self):
        """Test form rejects a date in the past."""
        past_date = date.today() - timedelta(days=1)
        form_data = {
            'name': 'Past Event',
            'description': 'Event in the past.',
            'date': past_date,
            'location': 'Old Location',
        }

        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())