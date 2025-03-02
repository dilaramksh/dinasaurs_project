from unicodedata import category

from django.test import TestCase
from django.urls import reverse

from social_media.models import *

from social_media.views import *


class SocietyPageViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        user = User.objects.create(
            first_name='john',
            last_name='doe',
            email='johndoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johndoe',
        )

        self.society = Society.objects.create(
            name='basketballclub',
            founder=user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=category,
            paid_membership=False,
        )

    def test_society_dashboard_view(self):
        #login_success = self.client.login(username='@janedoe', password='Password123') # society account
        #self.assertTrue(login_success)
        # check successful retrieval
        response = self.client.get(reverse('society_dashboard', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/society_dashboard.html')
        #self.assertIn('user', response.context)
        #self.assertEqual(response.context['user'].user_type, 'society')

    '''def test_event_creation_view(self):'''

    def test_terminate_society_view(self):
        #login_success = self.client.login(username='@janedoe', password='Password123')
        #self.assertTrue(login_success)
        response = self.client.get(reverse('terminate_society'))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'society/terminate_society.html')
        # check correct user type
        #self.assertIn('user', response.context) # should be society???
        #self.assertEqual(response.context['user'].user_type, 'student')

    def test_view_members_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        # login_success = self.client.login(username='@janedoe', password='Password123')
        # self.assertTrue(login_success)
        response = self.client.get(reverse('view_members'))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'society/view_members.html')
        # check correct user type
        # self.assertIn('user', response.context) # should be society???
        # self.assertEqual(response.context['user'].user_type, 'student')


    '''def test_view_upcoming_events_view(self):
        response = self.client.get(reverse('view_upcoming_events'))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'society/view_upcoming_events.html')'''

    '''def test_create_post_view(self):'''