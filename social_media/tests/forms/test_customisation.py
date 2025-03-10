from django.test import TestCase
from social_media.models.society import Society
from social_media.forms import customisationForm

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
        """Test if the form is valid with correct data."""
        form_data = {
            "name": "Tech Society Updated",
            "society_email": "updated@example.com",
            "description": "Updated description",
            "category": "Technology",
            "price": 15,
            "colour1": "#123456",
            "colour2": "#654321"
        }
        form = customisationForm(data=form_data, instance=self.society)
        self.assertTrue(form.is_valid())

    def test_empty_required_fields(self):
        """Test if the form is invalid when required fields are empty."""
        form_data = {
            "name": "",
            "society_email": "",
            "description": "",
            "category": "",
            "price": "",
            "colour1": "",
            "colour2": ""
        }
        form = customisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
        self.assertIn("society_email", form.errors)
        self.assertIn("description", form.errors)
        self.assertIn("category", form.errors)
        self.assertIn("price", form.errors)
        self.assertIn("colour1", form.errors)
        self.assertIn("colour2", form.errors)

    def test_invalid_email_format(self):
        """Test if the form rejects an invalid email format."""
        form_data = {
            "name": "Tech Society",
            "society_email": "invalid-email",
            "description": "A society for tech enthusiasts",
            "category": "Technology",
            "price": 10,
            "colour1": "#FF5733",
            "colour2": "#33FF57"
        }
        form = customisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("society_email", form.errors)

    def test_negative_price(self):
        """Test if the form rejects a negative price."""
        form_data = {
            "name": "Tech Society",
            "society_email": "tech@example.com",
            "description": "A society for tech enthusiasts",
            "category": "Technology",
            "price": -5, 
            "colour1": "#FF5733",
            "colour2": "#33FF57"
        }
        form = customisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_invalid_hex_color(self):
        """Test if the form rejects invalid hex color values."""
        form_data = {
            "name": "Tech Society",
            "society_email": "tech@example.com",
            "description": "A society for tech enthusiasts",
            "category": "Technology",
            "price": 10,
            "colour1": "INVALID_COLOR", 
            "colour2": "12345"  
        }
        form = customisationForm(data=form_data, instance=self.society)
        self.assertFalse(form.is_valid())
        self.assertIn("colour1", form.errors)
        self.assertIn("colour2", form.errors)
