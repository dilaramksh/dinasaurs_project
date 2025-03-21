from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_media.models import University, Society, Membership
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

User = get_user_model()

class MembershipViewsTestCase(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="KCL",
            domain="kcl.ac.uk",
            status="approved"
        )

        self.user = User.objects.create_user(
            username="@jane",
            email="jane@kcl.ac.uk",
            password="password123",
            university=self.university
        )

        self.society = Society.objects.create(
            name="Chess Club",
            founder=self.user,
            society_email="chess@kcl.ac.uk",
            description="Chess",
            category_id=1,  # You may need to mock a category
            paid_membership=False,
            status="approved",
            colour1="#000000",
            colour2="#FFFFFF"
        )

        self.view_memberships_url = reverse('view_memberships')
        self.join_society_url = reverse('join_society', args=[self.society.id])

    def test_view_memberships(self):
        Membership.objects.create(user=self.user, society=self.society, society_role=None)
        self.client.login(username='@jane', password='password123')
        response = self.client.get(self.view_memberships_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/memberships.html')
        self.assertIn('memberships', response.context)
        self.assertEqual(len(response.context['memberships']), 1)

    def test_join_society_success(self):
        self.client.login(username='@jane', password='password123')
        response = self.client.post(self.join_society_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        self.assertTrue(Membership.objects.filter(user=self.user, society=self.society).exists())

    def test_join_society_already_member(self):
        Membership.objects.create(user=self.user, society=self.society, society_role=None)
        self.client.login(username='@jane', password='password123')
        response = self.client.post(self.join_society_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False, "error": "You are already a member of this society."})

    def test_remove_membership_success(self):
        self.client.login(username='@jane', password='password123')
        membership = Membership.objects.create(user=self.user, society=self.society, society_role=None)
        response = self.client.post(reverse('remove_membership', args=[membership.id]))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "success": True,
            "society_name": self.society.name,
            "message": f"You have successfully left {self.society.name}."
        })
        self.assertFalse(Membership.objects.filter(id=membership.id).exists())

    def test_remove_membership_rejects_get(self):
        self.client.login(username='@jane', password='password123')
        membership = Membership.objects.create(user=self.user, society=self.society, society_role=None)
        response = self.client.get(reverse('remove_membership', args=[membership.id]))
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {
            "success": False,
            "error": "Only POST requests are allowed."
        })
