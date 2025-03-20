from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from social_media.models import Society, SocietyColorHistory
from social_media.forms import CustomisationForm


class CustomiseSocietyViewTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.society = Society.objects.create(
            name='Test Society', 
            description='Test description', 
            price=10.0, 
            colour1='#FFFFFF', 
            colour2='#000000'
        )
        self.url = reverse('customise_society', args=[self.society.id])

    def test_customise_society_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_customise_society_view_get_logged_in_user(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Customise Your Society')
        self.assertContains(response, 'Submit')
        self.assertContains(response, 'Current Society Details')

    def test_customise_society_view_post_valid_data_creates_colour_history(self):
        self.client.login(username='testuser', password='password123')
        form_data = {
            'description': 'Updated description',
            'price': 15.0,
            'colour1': '#FF0000',
            'colour2': '#00FF00',
        }
        
        response = self.client.post(self.url, form_data)
        
        self.society.refresh_from_db()
        self.assertEqual(self.society.description, 'Updated description')
        self.assertEqual(self.society.price, 15.0)
        self.assertEqual(self.society.colour1, '#FF0000')
        self.assertEqual(self.society.colour2, '#00FF00')
        
        past_color_history = SocietyColorHistory.objects.first()
        self.assertEqual(past_color_history.previous_colour1, '#FFFFFF')
        self.assertEqual(past_color_history.previous_colour2, '#000000')

        self.assertRedirects(response, reverse('society_mainpage', args=[self.society.id]))

    def test_customise_society_view_post_invalid_data(self):
        self.client.login(username='testuser', password='password123')
        form_data = {
            'description': '',  # Invalid empty description
            'price': 15.0,
            'colour1': '#FF0000',
            'colour2': '#00FF00',
        }
        
        response = self.client.post(self.url, form_data)
        
        self.assertFormError(response, 'form', 'description', 'This field is required.')

    def test_customise_society_view_logged_in_user_can_see_previous_colors(self):
        self.client.login(username='testuser', password='password123')
        
        # Create previous color history
        SocietyColorHistory.objects.create(
            society=self.society,
            previous_colour1='#FFFFFF',
            previous_colour2='#000000'
        )
        
        response = self.client.get(self.url)
        
        self.assertContains(response, 'Previous Colour History')
        self.assertContains(response, '#FFFFFF')
        self.assertContains(response, '#000000')
