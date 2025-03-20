from django.test import TestCase
from social_media.models.society import Society
from social_media.forms import CustomisationForm  

class CustomisationFormTest(TestCase):
    
    def setUp(self):
        """Set up a test society instance."""
        self.society = Society.objects.create(
            name="Tech Society",
            society_email="tech@example.com",
            description="A society for tech enthusiasts",
            category="Technology",
            price=10,
            colour1="#FF5733",
            colour2="#33FF57"
        )

    def test_valid_form(self):
        """Test if the form is valid with correct hex colors."""
        form_data = {
            "colour1": "#123456",
            "colour2": "#654321"
        }
        form = CustomisationForm(data=form_data, instance=self.society)
        self.assertTrue(form.is_valid())

    def test_empty_required_fields(self):
        """Test if the form is invalid when required fields are empty."""
        form_data = {
            "colour1": "",
            "colour2": ""
        }
        form = CustomisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("colour1", form.errors)
        self.assertIn("colour2", form.errors)

    def test_invalid_hex_color(self):
        """Test if the form rejects invalid hex color values."""
        form_data = {
            "colour1": "INVALID_COLOR",  
            "colour2": "12345"  
        }
        form = CustomisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("colour1", form.errors)
        self.assertIn("colour2", form.errors)
