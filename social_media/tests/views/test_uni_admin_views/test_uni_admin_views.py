from django.test import TestCase
from django.urls import reverse
from social_media.models import *
from django.contrib.messages import get_messages


class UniAdminViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        category = Category.objects.get_or_create(name='sports')

        self.uni_admin = User.objects.create_user(
            first_name='lebron',
            last_name='james',
            email='lebronjames@kcl.ac.uk',
            user_type='uni_admin',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@lebronjames',
            password='Password123'
        )
        self.uni_admin.save()
        self.login_url = reverse('log_in')

        self.student = User.objects.create_user(
            first_name='michael',
            last_name='jordan',
            email='michaeljordan@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@michaeljordan',
            password='Password123'
        )
        self.student.save()

        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.student,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=category,
            paid_membership=False,
            colour1='#FF0000',
            colour2='#00FF00'
        )

        self.society_role = SocietyRole.objects.create(
            society=self.society,
            role_name='President'
        )

        self.membership = Membership.objects.create(
            user=self.student,
            society=self.society,
            society_role=self.society_role

        )
        self.change_status_url = reverse('change_society_status', args=[self.society.id])




    def test_change_society_status_views(self):
        self.client.login(self.student.username, self.student.password)  # log in a student
        response = self.client.post(self.change_status_url, {'next_status': 'approved'})
        self.assertEqual(response.status_code, 403)  # forbidden

        self.client.login(self.uni_admin.username, self.uni_admin.password)  # Log in as uni_admin

        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'approved'})

        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "approved")

        society_role = SocietyRole.objects.get(society=self.society, role_name="President")
        membership = Membership.objects.get(user=self.student, society=self.society, society_role='President')
        self.assertRedirects(response, f"/dashboard/?status=approved")
        self.assertIsNotNone(membership)
        self.assertRedirects(response, f"/dashboard/?status=approved")


    '''def test_society_request_details(self):
    # log in as uni admn should fail
    # society founder should be from correct university
    #assert in context society'''



