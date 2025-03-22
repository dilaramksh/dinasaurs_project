from django.core.exceptions import ValidationError
from django.test import TestCase
from social_media.models import SocietyRole, Category, Society, User

class SocietyRoleModelTestCase(TestCase):
    """Unit tests for the Society Role Model"""
    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]
    def setUp(self):
        self.valid_role_name = "President"
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
            founder = User.objects.get(email="john.doe@test.ac.uk"),
            description="A desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="pending",
        )

    def test_create_valid_society_role(self):
        """Test creating a valid society role"""
        society_role = SocietyRole(society=self.society, role_name = self.valid_role_name)
        society_role.full_clean()
        society_role.save()
        self.assertEqual(SocietyRole.objects.count(), 1)

    def test_unique_role_within_a_society(self):
        """Test role_name and society make a unique combination"""
        SocietyRole.objects.create(society=self.society, role_name=self.valid_role_name)
        duplicate = SocietyRole(society=self.society, role_name=self.valid_role_name)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_empty_role_name(self):
        """Test an empty role_name raises ValidationError."""
        role = SocietyRole(society=self.society, role_name="")
        with self.assertRaises(ValidationError):
            role.full_clean()

    def test_str_method(self):
        """Test the __str__ method returns expected format."""
        role = SocietyRole.objects.create(society=self.society, role_name="Treasurer")
        self.assertEqual(str(role), f"{self.society.name} - Treasurer")

    def test_is_committee_role(self):
        """Test the is_committee_role method behavior."""
        committee_role = SocietyRole(society=self.society, role_name="President")
        member_role = SocietyRole(society=self.society, role_name="Member")
        self.assertTrue(committee_role.is_committee_role())
        self.assertFalse(member_role.is_committee_role())



