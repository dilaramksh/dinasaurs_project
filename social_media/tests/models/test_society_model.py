from django.test import TestCase
from social_media.models import Category, University, Society, User
from django.core.exceptions import ValidationError
from django.test import TestCase

class SocietyModelTestCase(TestCase):
    """Unit tests for the Society Model"""
    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]
    def setUp(self):
        self.category = Category.objects.create(name='cultural')
        self.university = University.objects.create(
            name="Test2 Univeristy", 
            domain="@test2.ac.uk"
            )
        
        self.valid_society_data = {
            "name": "A Soc",
            "society_email": "asoc@test.ac.uk",
            "founder": User.objects.get(email="john.doe@test.ac.uk"),
            "description": "A description.",
            "category": self.category,
            "paid_membership": False,
            "price": 0.0,
            "colour1": "#FFFFFF",
            "colour2": "#000000",
            "termination_reason": "operational",
            "status": "pending",
        }

    def test_create_valid_society(self):
        """Test creating a society with valid data."""
        society = Society(**self.valid_society_data)
        society.full_clean() 
        society.save()
        self.assertEqual(Society.objects.count(), 1)

    def test_unique_society_email(self):
        """Test that 'society_email' is unique."""
        Society.objects.create(**self.valid_society_data)
        duplicate = Society(
            name="Another Soc",
            society_email="asoc@test.ac.uk",
            founder = User.objects.get(email="john.doe@test.ac.uk"),
            description="Another desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="pending",
        )
        with self.assertRaises(ValidationError):
            duplicate.full_clean() 
            

    def test_invalid_hex_colour(self):
        """Test that an invalid hex colour raises ValidationError."""
        invalid_data = dict(self.valid_society_data, colour1="#ZZZZZZ")
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_price_exceeds_max(self):
        """Test that price > 50 raises ValidationError."""
        invalid_data = dict(self.valid_society_data, paid_membership=True, price=60.0)
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()    

    def test_free_membership_must_have_price_zero(self):
        invalid_data = dict(self.valid_society_data, price=10.0)
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_paid_membership_must_have_price_greater_than_zero(self):
        invalid_data = dict(self.valid_society_data, paid_membership=True, price=0.0)
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_negative_price_not_allowed(self):
        invalid_data = dict(self.valid_society_data, price=-10.0)
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_status_choices(self):
        """Test that an invalid status choice raises ValidationError."""
        invalid_data = dict(self.valid_society_data, status="nonexistent_status")
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_termination_reason_choices(self):
        """Test that invalid termination_reason raises ValidationError."""
        invalid_data = dict(self.valid_society_data, termination_reason="nonexistent_reason")
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

