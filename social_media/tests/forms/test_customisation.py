from django.test import TestCase
from social_media.forms import CustomisationForm  

class CustomisationFormTest(TestCase):
    """Test cases for the CustomisationForm."""

    def test_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'colour1': '#ff0000',
            'colour2': '#00ff00'
        }
        form = CustomisationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with invalid data."""
        form_data = {
            'colour1': 'not-a-color',
            'colour2': '#00ff00'
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('colour1', form.errors)

    def test_form_missing_data(self):
        """Test form with missing data."""
        form_data = {
            'colour1': '#ff0000'
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('colour2', form.errors)
        
    def test_form_empty_data(self):
        """Test form with empty data."""
        form_data = {}
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('colour1', form.errors)
        self.assertIn('colour2', form.errors)