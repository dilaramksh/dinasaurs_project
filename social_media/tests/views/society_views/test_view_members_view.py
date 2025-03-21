from django.test import TestCase, Client
from django.urls import reverse
from django.utils.timezone import now
from social_media.models import User, Society, Membership, SocietyRole, University, Category

class ViewMembersTests(TestCase):
    """Test cases for the view_members view."""

    def setUp(self):
        """Set up test data before each test."""
        self.client = Client()
        self.university = University.objects.create(name="Test University")
        self.category = Category.objects.create(name="Test Category")
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass',
            email='testuser1@example.com',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpass',
            email='testuser2@example.com',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
        self.user3 = User.objects.create_user(
            username='testuser3',
            password='testpass',
            email='testuser3@example.com',
            first_name='Test',
            last_name='User',
            user_type='student',
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
        )
        self.society = Society.objects.create(
            name="Test Society",
            founder=self.user1,
            society_email="test@society.com",
            description="A test society",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.role_committee = SocietyRole.objects.create(society=self.society, role_name="Committee")
        self.role_member = SocietyRole.objects.create(society=self.society, role_name="Member")
        Membership.objects.create(user=self.user1, society=self.society, society_role=self.role_committee)
        Membership.objects.create(user=self.user2, society=self.society, society_role=self.role_member)
        Membership.objects.create(user=self.user3, society=self.society, society_role=self.role_committee)

    def test_view_members_get(self):
        """Test the view_members view with GET request."""
        response = self.client.get(reverse('view_members', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/view_members.html')
        self.assertIn(self.user1, response.context['committee_members'])
        self.assertIn(self.user3, response.context['committee_members'])
        self.assertNotIn(self.user2, response.context['committee_members'])
        self.assertIn(self.user1, response.context['users'])
        self.assertIn(self.user2, response.context['users'])
        self.assertIn(self.user3, response.context['users'])
        self.assertEqual(response.context['society_id'], self.society.id)