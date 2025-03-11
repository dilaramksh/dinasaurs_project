from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from social_media.models import Event
from social_media.forms import EventCreationForm
'''
class EventCreationViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.url = reverse('event_creation')

    def test_event_creation_view_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_event_creation_view_post_valid_data(self):
        self.client.login(username='testuser', password='password123')
        event_data = {'title': 'Test Event', 'description': 'This is a test event description.'}

        response = self.client.post(self.url, event_data)

        self.assertEqual(Event.objects.count(), 1)
        event = Event.objects.first()
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'This is a test event description.')

        self.assertContains(response, 'Your event has been created.')
        self.assertRedirects(response, reverse('society_dashboard'))

    def test_event_creation_view_post_invalid_data(self):
        self.client.login(username='testuser', password='password123')
        event_data = {'title': '', 'description': ''}

        response = self.client.post(self.url, event_data)

        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'description', 'This field is required.')

        self.assertContains(response, 'Create a New Event')
        self.assertContains(response, 'Submit')

    def test_event_creation_view_logged_in_user_can_see_event_form(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.url)

        self.assertContains(response, 'Create a New Event')
        self.assertContains(response, 'Submit')
        self.assertContains(response, 'Event Description')
'''