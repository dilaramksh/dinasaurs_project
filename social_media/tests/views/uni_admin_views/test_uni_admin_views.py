from django.test import TestCase
from django.urls import reverse
from social_media.models import User, Society, SocietyRole, University, Membership, Category



class UniAdminViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London", status='approved', domain='@kcl.ac.uk')
        university2 = University.objects.create(name="University College London", status='approved', domain='@ucl.ac.uk')

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


        self.uni_admin2 = User.objects.create_user(
            first_name='scottie',
            last_name='pippen',
            email='scottiepippen@ucl.ac.uk',
            user_type='uni_admin',
            university=university2,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@scottiepippen',
            password='Password123'
        )

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

        self.category = Category.objects.create(
            name='sports'
        )

        self.society = Society.objects.create(
            name='basketballclub',
            founder=self.student,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=self.category,
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

        # URLs
        self.change_status_url = reverse('change_society_status', args=[self.society.id])
        self.request_details_url = reverse('society_request_details', args=[self.society.id])


    # PASSES
    def test_attempt_as_student_change_society_status_views(self):
        self.client.login(username='@michaeljordan', password='Password123')
        response = self.client.post(self.change_status_url)
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_attempt_as_admin_change_society_status_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'approved'})
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "approved")

    # PASSES
    def test_attempt_as_admin_change_society_status_other_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'other'})
        self.assertEqual(response.status_code, 302)
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "pending")
        self.assertRedirects(response, f"/dashboard/?status=pending")

    # PASSES
    def test_attempt_as_admin_change_society_status_blocked_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'blocked'})
        self.assertEqual(response.status_code, 302)
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "blocked")
        self.assertRedirects(response, f"/dashboard/?status=blocked")

    # PASSES
    def test_society_approval_creates_president_role(self):
        self.assertEqual(self.society.status, "pending")
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        response = self.client.post(self.change_status_url, {'next_status': 'approved'})
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "approved")
        president_role = SocietyRole.objects.filter(society=self.society, role_name="President").first()
        self.assertIsNotNone(president_role, "President role should be created.")
        membership = Membership.objects.filter(user=self.society.founder, society_role=president_role).first()
        self.assertIsNotNone(membership, "Founder should be assigned as President.")
        self.assertEqual(SocietyRole.objects.filter(society=self.society, role_name="President").count(), 1)
        self.assertEqual(Membership.objects.filter(user=self.society.founder, society_role=president_role).count(), 1)
        self.assertRedirects(response, f"/dashboard/?status=approved")

    # PASSES
    def test_attempt_as_student_society_request_details_view(self):
        login_success = self.client.login(username='@michaeljordan', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_attempt_as_other_uni_admin_society_request_details_view(self):
        login_success = self.client.login(username='@scottiepippen', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 403)

    # PASSES
    def test_society_request_details_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("uni_admin/society_request_details.html")
        self.assertIn('society', response.context)
