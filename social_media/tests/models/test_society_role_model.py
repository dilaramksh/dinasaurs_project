from django.core.exceptions import ValidationError
from django.test import TestCase
from social_media.models import SocietyRole, Category, Society

class SocietyRoleModelTestCase(TestCase):
    """Unit tests for the Society Role Model"""
        
    def setUp(self):
        self.valid_role_name = "President"
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
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


