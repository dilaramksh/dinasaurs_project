from django.test import TestCase
from django.core.exceptions import ValidationError
from social_media.models import User, Society, Membership, SocietyRole, Category, University
from datetime import date


class MembershipModelTest(TestCase):
    def setUp(self):
        # Set up a university and category
        self.university = University.objects.create(
            name="KCL",
            domain="kcl.ac.uk",
            status="approved",
            logo="university_logos/kcl.png"
        )

        self.category = Category.objects.create(name="Tech")

        # Create a user
        self.user = User.objects.create_user(
            username="@student1",
            email="student1@example.com",
            password="testpass123",
            university=self.university,
            start_date=date(2022, 9, 1),
            end_date=date(2026, 6, 30),
        )

        # Approved society
        self.society = Society.objects.create(
            name="Coding Club",
            founder=self.user,
            category=self.category,
            status="approved",
            logo="society_logos/code.png",
            society_email="codingclub@example.com"
        )

        # Non-approved society
        self.unapproved_society = Society.objects.create(
            name="Drama Club",
            founder=self.user,
            category=self.category,
            status="pending",
            logo="society_logos/drama.png",
            society_email="dramaclub@example.com"
        )

        # Society role
        self.committee_role = SocietyRole.objects.create(
            role_name="President",
            society=self.society
        )

    def test_create_valid_membership(self):
        membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.committee_role
        )
        self.assertEqual(str(membership), "@student1 - Coding Club (President)")

    def test_duplicate_membership_not_allowed(self):
        Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.committee_role
        )
        with self.assertRaises(Exception):
            Membership.objects.create(
                user=self.user,
                society=self.society,
                society_role=self.committee_role
            )

    def test_membership_in_unapproved_society_raises_validation_error(self):
        membership = Membership(
            user=self.user,
            society=self.unapproved_society,
            society_role=self.committee_role
        )
        with self.assertRaises(ValidationError):
            membership.clean()

    def test_is_committee_member_returns_true(self):
        membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.committee_role
        )
        self.assertTrue(membership.is_committee_member())

    def test_str_method(self):
        membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.committee_role
        )
        expected_str = "@student1 - Coding Club (President)"
        self.assertEqual(str(membership), expected_str)
