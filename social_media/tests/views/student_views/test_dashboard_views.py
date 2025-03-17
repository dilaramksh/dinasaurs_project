from django.test import TestCase
from django.urls import reverse
from social_media.models import *
from social_media.views import *

class DashboardViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category_name = 'sports'
        category, created = Category.objects.get_or_create(name=category_name)

        self.user = User.objects.create_user(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
            password='Password123'
        )
        self.login_url = reverse('log_in')

        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=category,
            paid_membership=False,
        )

        self.society_role = SocietyRole.objects.create(
            society=self.society,
            role_name='member'
        )

        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.society_role

        )

        self.login_url = reverse('log_in')
        self.dashboard_mainpage_url = reverse('dashboard_from_mainpage', args=[self.society.id])


    def test_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('student/student_dashboard.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')

    # FAILING
    def test_get_society_dashboard_view(self):
        response = self.client.get(reverse('society_dashboard', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/society_dashboard.html')
        self.assertIn('society', response.context)

    # PASSES
    def test_get_student_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)

        session = self.client.session
        session['active_society_id'] = 123
        session.save()

        self.assertIn('active_society_id', self.client.session)
        response = self.client.get(reverse('to_student_dashboard'))

        self.assertNotIn('active_society_id', self.client.session)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


