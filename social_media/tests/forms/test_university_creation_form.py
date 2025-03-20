from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from social_media.forms import UniversityCreationForm

class UniversityCreationFormTest(TestCase):
    def setUp(self):
        """Setup common form data for tests."""
        self.valid_data = {
            "name": "Test University",
            "domain": "test.ac.uk",
            "logo": "university_logos/default.png",
        }
        self.invalid_domain_data = {
            "name": "Test University",
            "domain": "invalid-domain",
        }
        self.missing_name_data = {
            "domain": "test.ac.uk",
        }
        
        self.missing_domain_data = {
            "name": "Test University",
        }

    def test_valid_form(self):
        """Test that form is valid with correct data."""
        form = UniversityCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        """Test that form is invalid when name is missing."""
        form = UniversityCreationForm(data=self.missing_name_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_domain(self):
        """Test that form is invalid when domain is missing."""
        form = UniversityCreationForm(data=self.missing_domain_data)
        self.assertFalse(form.is_valid())
        self.assertIn("domain", form.errors)

    def test_optional_logo(self):
        """Test that form is valid without a logo."""
        form = UniversityCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_invalid_domain(self):
        """Test that form is invalid with an improperly formatted domain."""
        form = UniversityCreationForm(data=self.invalid_domain_data)
        self.assertFalse(form.is_valid())
        self.assertIn("domain", form.errors)
