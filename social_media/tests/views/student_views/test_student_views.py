import self
from django.test import TestCase, Client
from django.urls import reverse
from social_media.models import User, University
from datetime import datetime

from social_media.student_views import student_dashboard


class StudentDashBoardViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name='kcl')

        self.user = User.objects.create(
            first_name= 'Jane',
            last_name= 'Doe',
            email = 'janedoe@email.com',
            user_type= 'student',
            university= university,
            start_date= '2023-09-23',
            end_date= '2026-05-06',

        )

    def test_student_dashboard_view(self):
        # check student has successfully been logged in
        login_success = self.client.login(username='janedoe@gmail.com', password='password123')
        self.assertTrue(login_success)

        # check that the student is able to access the dashboard
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)

        # check that it is the correct template
        self.assertTemplateUsed(response, 'student/student_dashboard.html')

        # check that the user accessing the page is a student
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], 'student')




