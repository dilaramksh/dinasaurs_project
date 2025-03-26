from django.conf import settings
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from social_media.models import Society, Membership, SocietyRole, User, Category
from unittest.mock import MagicMock, patch
from social_media.helpers import (
    login_prohibited, membership_required, committee_required,
    get_committee_members, is_user_committee, redirect_to_society_dashboard
)


class HelpersTestSuite(TestCase):
    fixtures = ['social_media/tests/fixtures/default_user.json', 'social_media/tests/fixtures/other_users.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')

        self.category = Category.objects.create(
            name='sports'
        )
        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            status='approved',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        self.society_role_member = SocietyRole.objects.create(role_name='member', society=self.society)
        self.society_role_committee = SocietyRole.objects.create(role_name='presidet', society=self.society)
        self.membership = Membership.objects.create(user=self.user, society=self.society, society_role=self.society_role_member)

    def test_login_prohibited_redirects_authenticated_user(self):
        request = self.factory.get('/')
        request.user = self.user

        @login_prohibited
        def mock_view(request):
            return "View accessed"

        response = mock_view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN))

    def test_login_prohibited_allows_anonymous_user(self):
        request = self.factory.get('/')
        request.user = AnonymousUser()

        @login_prohibited
        def mock_view(request):
            return "View accessed"

        response = mock_view(request)
        self.assertEqual(response, "View accessed")

    def test_membership_required_redirects_if_not_a_member(self):
        request = self.factory.get('/')
        request.user = self.other_user

        @membership_required
        def mock_view(request, society_id):
            return "View accessed"

        response = mock_view(request, self.society.id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))

    def test_membership_required_allows_member_access(self):
        request = self.factory.get('/')
        request.user = self.user

        @membership_required
        def mock_view(request, society_id):
            return "View accessed"

        response = mock_view(request, self.society.id)
        self.assertEqual(response, "View accessed")

    def test_committee_required_raises_permission_denied_for_non_committee(self):
        request = self.factory.get('/')
        request.user = self.user

        @committee_required
        def mock_view(request, society_id):
            return "View accessed"

        with self.assertRaises(PermissionDenied):
            mock_view(request, self.society.id)

    def test_committee_required_allows_committee_access(self):
        self.membership.society_role = self.society_role_committee
        self.membership.save()

        request = self.factory.get('/')
        request.user = self.user

        @committee_required
        def mock_view(request, society_id):
            return "View accessed"

        response = mock_view(request, self.society.id)
        self.assertEqual(response, "View accessed")

    def test_get_committee_members_returns_committee_members(self):
        self.membership.society_role = self.society_role_committee
        self.membership.save()

        with patch.object(Membership, 'is_committee_member', return_value=True):
            members = get_committee_members(self.society)
            self.assertIn(self.user, members)

    def test_is_user_committee_returns_true_for_committee_member(self):
        self.membership.society_role = self.society_role_committee
        self.membership.save()

        with patch.object(Membership, 'is_committee_member', return_value=True):
            self.assertTrue(is_user_committee(self.user, self.society))

    def test_is_user_committee_returns_false_for_non_member(self):
        self.assertFalse(is_user_committee(self.other_user, self.society))

    def test_redirect_to_society_dashboard_redirects_to_active_society(self):
        request = self.factory.get('/')
        request.session = {'active_society_id': self.society.id}

        response = redirect_to_society_dashboard(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('society_dashboard', args=[self.society.id]))

    def test_redirect_to_society_dashboard_falls_back_to_dashboard(self):
        request = self.factory.get('/')
        request.session = {}

        response = redirect_to_society_dashboard(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard'))
