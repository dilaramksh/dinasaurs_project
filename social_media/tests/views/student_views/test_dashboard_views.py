from django.test import TestCase
from django.urls import reverse
from social_media.models import *
from social_media.views import *

class DashboardViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        user = User.objects.create(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
        )
        self.login_url = reverse('log_in')

        self.society = Society.objects.create(
            name='basketballclub',
            founder=user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=category,
            paid_membership=False,
        )

    def test_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('student/student_dashboard.html')
        self.assertIn('user', response.context)
        #self.assertEqual(response.context['user'].user_type, 'student')

    '''def test_get_society_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('get_society_dashboard', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('society/society_dashboard.html')
        #self.assertIn('user', response.context)
'''
