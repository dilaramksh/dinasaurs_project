from django.test import TestCase
from django.urls import reverse
from social_media.models import User, University

class UniAdminViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")

        self.user = User.objects.create(
            first_name='paul',
            last_name='poe',
            email='paulpoe@kcl.ac.uk',
            user_type='uni_admin',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@paulpoe',
        )
        self.user.set_password('Password123')
        self.user.save()
        self.login_url = reverse('log_in')



    def test_change_society_status(self):
        login_success = self.client.login(username='@paulpoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('change_society_status'))
        self.assertEqual(response.status_code, 200)
        '''self.assertTemplateUsed(response, 'student/student_dashboard.html')'''
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'uni_admin')


    def test_society_request_details(self):
        login_success = self.client.login(username='@paulpoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('society_request_details'))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'uni_admin/society_request_details.html')
        # check correct user type
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'uni_admin')


