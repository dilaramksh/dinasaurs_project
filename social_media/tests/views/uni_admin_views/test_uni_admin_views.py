from django.test import TestCase
from django.urls import reverse
from social_media.models import User, Society, SocietyRole, University, Membership, Category



class UniAdminViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(
            name="King's College London",
            status='approved',
            domain='@kcl.ac.uk')

        university2 = University.objects.create(
            name="University College London",
            status='approved',
            domain='@ucl.ac.uk')

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

        self.student2 = User.objects.create_user(
            first_name='dennis',
            last_name='rodman',
            email='dennisrodman@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@dennisrodman',
            password='Password123'
        )

        self.student3 = User.objects.create_user(
            first_name='bronny',
            last_name='james',
            email='bronnyjames@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@bronnyjames',
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

        self.society2 = Society.objects.create(
            name='betterbasketballclub',
            founder=self.student2,
            society_email='betterbasketballclub@kcl.ac.uk',
            description='basketball club but better',
            category=self.category,
            paid_membership=False,
            colour1='#FF0000',
            colour2='#00FF00'
        )

        self.society3 = Society.objects.create(
            name='evenbetterbasketballclub',
            founder=self.student3,
            society_email='evenbetterbasketballclub@kcl.ac.uk',
            description='even basketball club but better',
            category=self.category,
            paid_membership=False,
            colour1='#FF0000',
            colour2='#00FF00'
        )

        self.society_role = SocietyRole.objects.create(
            society=self.society,
            role_name='President'
        )

        self.society_role2 = SocietyRole.objects.create(
            society=self.society2,
            role_name='Secretary'
        )


        self.president_role = SocietyRole.objects.create(
            society=self.society2,
            role_name='President'
        )

        self.membership = Membership.objects.create(
            user=self.student,
            society=self.society,
            society_role=self.society_role

        )

        self.membership2 = Membership.objects.create(
            user=self.student2,
            society=self.society2,
            society_role=self.society_role2

        )

        # URLs
        self.change_status_url = reverse('change_society_status', args=[self.society.id])
        self.change_status_url2 = reverse('change_society_status', args=[self.society2.id])
        self.change_status_url3 = reverse('change_society_status', args=[self.society3.id])
        self.request_details_url = reverse('society_request_details', args=[self.society.id])



    def test_attempt_as_student_change_society_status_views(self):
        self.client.login(username='@michaeljordan', password='Password123')
        response = self.client.post(self.change_status_url)
        self.assertEqual(response.status_code, 403)


    def test_attempt_as_admin_change_society_status_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'approved'})
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "approved")


    def test_attempt_as_admin_change_society_status_other_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'other'})
        self.assertEqual(response.status_code, 302)
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "pending")
        self.assertRedirects(response, f"/dashboard/?status=pending")


    def test_attempt_as_admin_change_society_status_blocked_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.society.status, "pending")
        response = self.client.post(self.change_status_url, {'next_status': 'blocked'})
        self.assertEqual(response.status_code, 302)
        self.society.refresh_from_db()
        self.assertEqual(self.society.status, "blocked")
        self.assertRedirects(response, f"/dashboard/?status=blocked")


    def test_assign_president_change_society_status_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        initial_membership_count = Membership.objects.count()
        existing_membership = Membership.objects.get(user=self.society2.founder, society=self.society2)
        self.assertNotEqual(existing_membership.society_role, self.president_role)
        response = self.client.post(self.change_status_url2, {'next_status': 'approved'})
        self.society2.refresh_from_db()
        existing_membership.refresh_from_db()
        self.assertEqual(self.society2.status, "approved")
        self.assertEqual(existing_membership.society_role, self.president_role)
        self.assertEqual(Membership.objects.count(), initial_membership_count)
        self.assertRedirects(response, f"/dashboard/?status=approved")

    def test_create_membership_if_not_existing(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(Membership.objects.filter(user=self.society3.founder, society=self.society3).count(), 0)
        initial_membership_count = Membership.objects.count()
        response = self.client.post(self.change_status_url3, {'next_status': 'approved'})
        self.society3.refresh_from_db()
        self.assertEqual(self.society3.status, 'approved')
        self.assertEqual(Membership.objects.count(), initial_membership_count + 1)
        created_membership = Membership.objects.get(user=self.society3.founder, society=self.society3)
        self.assertEqual(created_membership.society_role.role_name, 'President')
        self.assertRedirects(response, f"/dashboard/?status=approved")


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


    def test_attempt_as_student_society_request_details_view(self):
        login_success = self.client.login(username='@michaeljordan', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 403)


    def test_attempt_as_other_uni_admin_society_request_details_view(self):
        login_success = self.client.login(username='@scottiepippen', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 403)


    def test_society_request_details_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.request_details_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("uni_admin/society_request_details.html")
        self.assertIn('society', response.context)


    def test_method_not_allowed(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(self.change_status_url)
        self.assertEqual(response.status_code, 405)
