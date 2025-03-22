from django.core.exceptions import ValidationError
from django.test import TestCase
from social_media.models import University

class UniversityModelTestCase(TestCase):
    """Unit tests for the University Model"""

    def setUp(self):
        # Setup some initial valid data
        self.valid_name = "Test University"
        self.valid_domain = "testuni.ac.uk"

    def test_create_valid_university(self):
        """Test that a university with valid name and domain can be created."""
        university = University(name=self.valid_name, domain=self.valid_domain)
        university.full_clean()  # Should not raise ValidationError
        university.save()
        self.assertEqual(University.objects.count(), 1)

    def test_name_uniqueness(self):
        """Test that the name field must be unique."""
        University.objects.create(name=self.valid_name, domain=self.valid_domain)
        duplicate = University(name=self.valid_name, domain="@different.ac.uk")
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_domain_uniqueness(self):
        """Test that the domain field must be unique."""
        University.objects.create(name=self.valid_name, domain=self.valid_domain)
        duplicate = University(name="Another University", domain=self.valid_domain)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_invalid_domain_too_short(self):
        """Test that a domain with fewer than 3 characters before '.ac.uk' raises a validation error."""
        invalid_domain = "@te.ac.uk"
        university = University(name="Short Domain University", domain=invalid_domain)
        with self.assertRaises(ValidationError):
            university.full_clean()

    def test_invalid_domain_missing_ac_uk(self):
        """Test that a domain not ending in '.ac.uk' raises a validation error."""
        invalid_domain = "@test.com"
        university = University(name="Invalid Suffix University", domain=invalid_domain)
        with self.assertRaises(ValidationError):
            university.full_clean()

    def test_valid_domain_edge_case(self):
        """Test that a domain with exactly 3 characters before '.ac.uk' is valid."""
        valid_domain = "@abc.ac.uk"
        university = University(name="Edge Case University", domain=valid_domain)
        university.full_clean()  # Should not raise ValidationError
        university.save()
        self.assertEqual(University.objects.count(), 1)

    def test_empty_name(self):
        """Test that an empty name raises a validation error."""
        university = University(name="", domain=self.valid_domain)
        with self.assertRaises(ValidationError):
            university.full_clean()

    def test_empty_domain(self):
        """Test that an empty domain raises a validation error."""
        university = University(name="Empty Domain University", domain="")
        with self.assertRaises(ValidationError):
            university.full_clean()

    def test_whitespace_in_domain(self):
        """Test that a domain containing whitespace raises a validation error."""
        invalid_domain = "@test .ac.uk"
        university = University(name="Whitespace Domain University", domain=invalid_domain)
        with self.assertRaises(ValidationError):
            university.full_clean()

    def test_str_method_returns_name(self):
        university = University.objects.create(name="Test Uni", domain="testuni.ac.uk")
        self.assertEqual(str(university), "Test Uni")

