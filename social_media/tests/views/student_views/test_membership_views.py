from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_media.models import Society, Membership, SocietyRole, University
from datetime import date
from social_media.models import Category

User = get_user_model()

class MembershipViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.university = University.objects.create(
            name="Hive Uni", domain="hiveuni.ac.uk", status="approved"
        )

        self.user = User.objects.create_user(
            username='@testuser',
            email='test@example.com',
            password='testpassword',
            university=self.university,
            start_date=date(2023, 1, 1),
            end_date=date(2027, 1, 1)
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="sports")

        self.society = Society.objects.create(
            name="Chess Club",
            status="approved",
            logo="society_logos/chess.png",
            category=self.category,
            founder=self.user
        )

        self.role = SocietyRole.objects.create(
            society=self.society,
            role_name="Member"
        )

    def test_view_memberships(self):
        Membership.objects.create(user=self.user, society=self.society, society_role=self.role)
        response = self.client.get(reverse('view_memberships'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chess Club")

    def test_join_society_success(self):
        response = self.client.post(reverse('dashboard_from_mainpage', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'Successfully joined society.'})
        self.assertTrue(Membership.objects.filter(user=self.user, society=self.society).exists())

    def test_join_society_already_member(self):
        Membership.objects.create(user=self.user, society=self.society, society_role=self.role)
        response = self.client.post(reverse('dashboard_from_mainpage', args=[self.society.id]))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'success': False, 'error': 'You are already a member of this society.'})

    def test_remove_membership_success(self):
        membership = Membership.objects.create(user=self.user, society=self.society, society_role=self.role)
        response = self.client.post(reverse('remove_membership', args=[membership.id]), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Membership.objects.filter(id=membership.id).exists())
        self.assertJSONEqual(response.content, {
            "success": True,
            "society_name": "Chess Club",
            "message": "You have successfully left Chess Club."
        })

    def test_remove_membership_rejects_get(self):
        membership = Membership.objects.create(user=self.user, society=self.society, society_role=self.role)
        response = self.client.get(reverse('remove_membership', args=[membership.id]))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {"success": False, "error": "Only POST requests are allowed."})
