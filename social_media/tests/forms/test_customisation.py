from django.test import TestCase
from social_media.forms import CustomisationForm

class CustomisationFormTest(TestCase):
    def test_valid_colours(self):
        """Test that the form is valid with correct hex color codes."""
        form_data = {
            "colour1": "#FF5733",
            "colour2": "#33FF57",
        }
        form = CustomisationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_colour1(self):
        """Test that the form is invalid when colour1 is not a valid hex code."""
        form_data = {
            "colour1": "red",  # Invalid format
            "colour2": "#33FF57",
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("colour1", form.errors)

    def test_invalid_colour2(self):
        """Test that the form is invalid when colour2 is not a valid hex code."""
        form_data = {
            "colour1": "#FF5733",
            "colour2": "blue",  # Invalid format
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("colour2", form.errors)

    def test_missing_colours(self):
        """Test that the form is invalid when one or both colour fields are missing."""
        form_data = {
            "colour1": "#FF5733",
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("colour2", form.errors)

    def test_empty_colours(self):
        """Test that the form is invalid when colours are empty strings."""
        form_data = {
            "colour1": "",
            "colour2": "",
        }
        form = CustomisationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("colour1", form.errors)
        self.assertIn("colour2", form.errors)
