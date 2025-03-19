from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_media.models import Society, Membership, SocietyRole, User

class ViewMembersTests(TestCase):

    def setUp(self):

        self.user_1 = get_user_model().objects.create_user(username="user1", email="user1@example.com")
        self.user_2 = get_user_model().objects.create_user(username="user2", email="user2@example.com")
  
        self.society = Society.objects.create(name="Test Society")
        
        self.committee_role = SocietyRole.objects.create(role_name="Committee Member")
        self.member_role = SocietyRole.objects.create(role_name="Member")

        self.membership_1 = Membership.objects.create(user=self.user_1, society=self.society, society_role=self.committee_role)
        self.membership_2 = Membership.objects.create(user=self.user_2, society=self.society, society_role=self.member_role)

        self.url = reverse('view_members', args=[self.society.id])

    def test_view_members_rendering(self):
        """Test that the view renders correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/view_members.html')

    def test_view_members_context(self):
        """Test that the correct context is passed to the view."""
        response = self.client.get(self.url)
 
        self.assertIn('committee_members', response.context)
        self.assertEqual(len(response.context['committee_members']), 1)
        self.assertEqual(response.context['committee_members'][0], self.user_1)


        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), 2)
        self.assertIn(self.user_1, response.context['users'])
        self.assertIn(self.user_2, response.context['users'])

    def test_search_functionality(self):
        """Test if the search functionality works as expected."""
        response = self.client.get(self.url, {'searchInput': 'user1'})

        self.assertContains(response, 'user1')
        self.assertNotContains(response, 'user2')

    def test_no_members_in_society(self):
        """Test if no members are displayed if there are no memberships."""

        empty_society = Society.objects.create(name="Empty Society")
        url = reverse('view_members', args=[empty_society.id])
        
        response = self.client.get(url)
        self.assertContains(response, "No users found.")

    def test_modal_for_each_user(self):
        """Test if each user has a modal in the response."""
        response = self.client.get(self.url)

        self.assertContains(response, f'id="userModal{self.user_1.id}"')
        self.assertContains(response, f'id="userModal{self.user_2.id}"')

    def test_committee_member_role_in_context(self):
        """Test if committee members are correctly displayed in the context."""
        response = self.client.get(self.url)

        self.assertContains(response, "Committee Member")

    def test_non_committee_member_role_not_displayed_as_committee(self):
        """Test that non-committee members do not show in the committee section."""
        response = self.client.get(self.url)

 
        self.assertNotContains(response, "Committee Member")

    def test_view_members_unauthenticated(self):
        """Test if unauthenticated users are redirected to login."""
        self.client.logout()
        
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/login/?next={self.url}")

    def test_search_no_results(self):
        """Test search when no members match the query."""
        response = self.client.get(self.url, {'searchInput': 'nonexistentuser'})
        
        # Check if the correct message appears for no results
        self.assertContains(response, "No users found.")
    
