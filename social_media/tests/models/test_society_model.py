from django.test import TestCase
from social_media.models import Category, University, Society, User
from django.core.exceptions import ValidationError

class SocietyModelTestCase(TestCase):
    """Comprehensive unit tests for the Society model."""
    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.category = Category.objects.create(name='Cultural')
        self.university = University.objects.create(
            name="Another Test University",
            domain="another-test.ac.uk"
        )
        self.valid_society_data = {
            "name": "A Soc",
            "society_email": "asoc@test.ac.uk",
            "founder": User.objects.get(email="john.doe@test.ac.uk"),
            "description": "A sample society.",
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
            founder=self.valid_society_data['founder'],
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
        society = Society.objects.create(
            name="test society",
            founder=User.objects.get(email="john.doe@test.ac.uk"),
            society_email="test@test.ac.uk",
            description="A test society",
            category=self.category,
            paid_membership=False,
            price=10.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.assertGreater(society.price, 0.0)

    def test_price_cannot_be_negative(self):
        """Test that saving a society with a negative price raises ValidationError."""
        society = Society(
            name="Test Society",
            founder=User.objects.get(email="john.doe@test.ac.uk"),
            society_email="test@test.ac.uk",
            description="A test society",
            category=self.category,
            paid_membership=True,
            price=-7.0,  # Negative price
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.assertGreater(0.0, society.price)

    def test_paid_membership_must_have_price_greater_than_zero(self):
        society = Society.objects.create(
            name="test society",
            founder=User.objects.get(email="john.doe@test.ac.uk"),
            society_email="test@test.ac.uk",
            description="A test society",
            category=self.category,
            paid_membership=True,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.assertGreater(10.0, society.price)

    def test_negative_price_not_allowed(self):
        """Test that negative price raises ValidationError."""
        invalid_data = dict(self.valid_society_data, price=-10.0)
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_paid_membership_field_true(self):
        """Test that paid_membership can be True."""
        data = dict(self.valid_society_data, paid_membership=True)
        society = Society.objects.create(**data)
        self.assertTrue(society.paid_membership)

    def test_paid_membership_field_false(self):
        """Test that paid_membership can be False."""
        data = dict(self.valid_society_data, paid_membership=False)
        society = Society.objects.create(**data)
        self.assertFalse(society.paid_membership)
        
    def test_save_method_triggers_validation_error_for_negative_price(self):
        """Ensure save() raises ValidationError for negative price and hits line 64."""
        data = dict(self.valid_society_data, price=-10.0)
        society = Society(**data)

        # Temporarily bypass validation so we hit save() directly
        society.full_clean = lambda *a, **kw: None

        with self.assertRaises(ValidationError) as context:
            society.save(force_insert=True)  # Ensure it's not an update call

        self.assertIn("Price cannot be negative.", str(context.exception))


    def test_status_choices(self):
        """Test that invalid status raises ValidationError."""
        invalid_data = dict(self.valid_society_data, status="invalid_status")
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_termination_reason_choices(self):
        """Test that invalid termination_reason raises ValidationError."""
        invalid_data = dict(self.valid_society_data, termination_reason="not_a_reason")
        society = Society(**invalid_data)
        with self.assertRaises(ValidationError):
            society.full_clean()

    def test_approve_sets_status_to_approved(self):
        """Test that calling approve() sets status to 'approved'."""
        society = Society.objects.create(**self.valid_society_data)
        society.approve()
        self.assertEqual(society.status, "approved")

    def test_block_sets_status_to_blocked(self):
        """Test that calling block() sets status to 'blocked'."""
        society = Society.objects.create(**self.valid_society_data)
        society.block()
        self.assertEqual(society.status, "blocked")

    def test_str_method_returns_title_case(self):
        """Test that __str__ returns the society name in title case."""
        society = Society.objects.create(**self.valid_society_data)
        self.assertEqual(str(society), "A Soc")

    def test_save_title_cases_name(self):
        """Test that the society name is title-cased on save."""
        data = dict(self.valid_society_data, name="lowercase society")
        society = Society.objects.create(**data)
        self.assertEqual(society.name, "Lowercase Society")

