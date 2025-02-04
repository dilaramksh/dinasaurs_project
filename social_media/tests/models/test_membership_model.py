from django.test import TestCase
from social_media.models import Category, Society, SocietyRole, User, Membership
from django.core.exceptions import ValidationError
from django.test import TestCase


class MembershipModelTestCase(TestCase):
    """Unit tests for the Membership Model"""
    
    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]

    def setUp(self):
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
        self.user = User.objects.get(email="john.doe@test.ac.uk")
        self.society_role = SocietyRole.objects.create(society=self.society, role_name="MyRole")

    def test_create_valid_membership(self):
        membership = Membership(user=self.user, society_role=self.society_role)
        membership.full_clean() 
        membership.save()
        self.assertEqual(Membership.objects.count(), 1)

    def test_unique_membership_within_society(self):
        """Test user and society role only make unique combinations."""
        Membership.objects.create(user=self.user, society_role=self.society_role)
        duplicate = Membership(user=self.user, society_role=self.society_role)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()
        
