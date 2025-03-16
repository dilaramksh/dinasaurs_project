from unicodedata import category

from django.test import TestCase
from django.urls import reverse

from social_media.models import *

from social_media.views import *
from social_media.views.society_views import society_dashboard


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
        self.society.save()

        self.form_data = {
            'name':'nba finals',
            #'society':society,
            'description':'nba finals watch party',
            'date':'2025-06-01',
            'location':'bush house lecture theatre',
            'society_id':self.society.id,
        }


        self.url = reverse('event_creation', kwargs={'society_id': self.society.id})

    def test_society_dashboard_view(self):
        response = self.client.get(reverse('get_society_dashboard'), kwargs={'society_id':self.society.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/society_dashboard.html')


    def test_get_event_creation_view(self):
        response = self.client.get(reverse('event_creation', kwargs={'society_id':self.society.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/event_creation.html')

    def test_post_event_creation_view(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.post(self.url, data=self.form_data)
        self.assertRedirects(response, reverse('get_society_dashboard', kwargs={'society_id': self.society.id}))
        created_event = Event.objects.filter(name='nba finals')
        self.assertTrue(created_event.exists())
        test_event = created_event.first()
        self.assertEqual(test_event.name, self.form_data['name'])
        self.assertEqual(test_event.society.id, self.society.id)
        self.assertEqual(test_event.description, self.form_data['description'])
        self.assertEqual(test_event.date, self.form_data['date'])
        self.assertEqual(test_event.location, self.form_data['location'])

    def test_terminate_society_view(self):

        response = self.client.get(reverse('terminate_society'))
        self.assertEqual(response.status_code, 200)
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