from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from social_media.models import Society, Membership
'''
User = get_user_model()

class TerminateSocietyViewTest(TestCase):
    def setUp(self):
        """Set up test data before each test."""

        self.user = User.objects.create_user(
            username="testuser", 
            password="testpass"
        )
        
        self.society = Society.objects.create(
            name="Test Society", 
            description="A test society"
        )
        
        self.client = Client()
        self.client.login(username="testuser", password="testpass")
        
      
        session = self.client.session
        session['active_society_id'] = self.society.id
        session.save()
        
        self.url = reverse('terminate_society', args=[self.society.id])

    def test_terminate_society_get(self):
        """Test if the termination confirmation page loads correctly."""
        response = self.client.get(self.url)
   
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/terminate_society.html')
        
        self.assertTrue(Society.objects.filter(id=self.society.id).exists())

    def test_terminate_society_post(self):
        """Test if society is deleted on POST request."""
      
        society_id = self.society.id
        
        response = self.client.post(self.url)
        
        self.assertRedirects(response, reverse("dashboard"))
        
        self.assertFalse(Society.objects.filter(id=society_id).exists())
        
        self.assertNotIn('active_society_id', self.client.session)

    def test_terminate_society_invalid_id(self):
        """Test behavior with non-existent society ID."""
       
        invalid_url = reverse('terminate_society', args=[9999])
        
        response = self.client.get(invalid_url)
       
        self.assertEqual(response.status_code, 404)

    def test_terminate_society_unauthenticated(self):
        """Test behavior when user is not authenticated."""

        self.client.logout()
        
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        
        # Society should still exist
        self.assertTrue(Society.objects.filter(id=self.society.id).exists())

    def test_terminate_society_with_memberships(self):
        """Test if society deletion also removes associated memberships."""
        # Create a membership for the society
        Membership.objects.create(
            user=self.user,
            society=self.society
        )
        self.assertTrue(Membership.objects.filter(society=self.society).exists())
        self.client.post(self.url)
        self.assertFalse(Membership.objects.filter(society=self.society).exists())

    def test_terminate_society_clears_session(self):
        """Test if terminating a society removes it from session."""
        # Ensure active_society_id is in session
        session = self.client.session
        session['active_society_id'] = self.society.id
        session.save()

        self.client.post(self.url)

        self.assertNotIn('active_society_id', self.client.session)
'''