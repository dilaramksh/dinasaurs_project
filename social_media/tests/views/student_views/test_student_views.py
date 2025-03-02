from django.test import TestCase
from django.urls import reverse

from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import User, University

class StudentDashBoardViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")

        self.user = User.objects.create(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
        )
        self.user.set_password('Password123')
        self.user.save()
        self.login_url = reverse('log_in')


    def test_student_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        # check successful login
        self.assertTrue(login_success)
        # check successful retrieval
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # check correct template
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        # check correct user type
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')


    """def test_help_view(self):
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('student/help.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')"""

    def test_society_browser_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('society_browser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('student/society_browser.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')



    """def test_society_creation_request(self):
        # form creation


        # form is successfully submitted
        response = self.client.post()
        self.assertEqual(response.status_code, 200)"""









