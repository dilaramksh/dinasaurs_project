from django.test import TestCase
from django.urls import reverse
from social_media.models import *
from social_media.views import *

class DashboardViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(
            name="King's College London",
            status='approved',
            domain='kcl.ac.uk')

        university2 = University.objects.create(
            name="SOAS",
            status='other',
            domain='@soas.ac.uk')

        self.student = User.objects.create_user(
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

        self.student2 = User.objects.create_user(
            first_name='john',
            last_name='doe',
            email='johndoe@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johndoe',
            password='Password123'
        )

        self.uni_admin = User.objects.create_user(
            first_name='michael',
            last_name='jordan',
            email='michaeljordan@kcl.ac.uk',
            user_type='uni_admin',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@michaeljordan',
            password='Password123'
        )

        self.uni_admin2 = User.objects.create_user(
            first_name='paul',
            last_name='poe',
            email='paulpoe@soas.ac.uk',
            user_type='uni_admin',
            university=university2,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@paulpoe',
            password='Password123'
        )

        self.super_admin = User.objects.create_user(
            first_name='lebron',
            last_name='james',
            email='lebronjames@kcl.ac.uk',
            user_type='super_admin',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@lebronjames',
            password='Password123'
        )

        self.other_user = User.objects.create_user(
            first_name='james',
            last_name='cordon',
            email='jamescordon@kcl.ac.uk',
            user_type='other',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@jamescordon',
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
        )

        self.society2 = Society.objects.create(
            name='footballclub',
            founder=self.student2,
            society_email='footballclub@kcl.ac.uk',
            description='footballclub',
            category=self.category,
            paid_membership=False,
        )

        self.society_role = SocietyRole.objects.create(
            society=self.society,
            role_name='member'
        )

        self.membership = Membership.objects.create(
            user=self.student,
            society=self.society,
            society_role=self.society_role

        )

        # URLs
        self.dashboard_mainpage_url = reverse('dashboard_from_mainpage', args=[self.society.id])


    def test_no_active_society_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        self.client.session['active_society_id'] = None
        self.client.session.save()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')


    def test_active_society_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        session = self.client.session
        session['active_society_id'] = 1
        session.save()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('society_dashboard', kwargs={'society_id': 1}))


    def test_approved_uni_admin_society_dashboard_view(self):
        login_success = self.client.login(username='@michaeljordan', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'uni_admin/uni_admin_dashboard.html')
        self.assertIn('societies', response.context)
        self.assertIn('chosen_status', response.context)
        self.assertEqual(response.context['user'].user_type, 'uni_admin')


    def test_invalid_status_uni_admin_dashboard_view(self):
        login_success = self.client.login(username='@paulpoe', password='Password123')
        self.assertTrue(login_success)
        self.assertEqual(self.uni_admin2.university.status, 'other')
        response = self.client.get(reverse('dashboard')  + '?status=invalid_status')
        self.assertEqual(response.status_code, 200)
        self.assertIn('societies', response.context)
        self.assertIn('chosen_status', response.context)
        self.assertEqual(response.context['chosen_status'], 'pending')
        self.assertTemplateUsed(response, 'uni_admin/uni_admin_dashboard.html')
        self.assertEqual(response.context['user'].user_type, 'uni_admin')


    def test_super_admin_society_dashboard_view(self):
        login_success = self.client.login(username='@lebronjames', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'super_admin/super_admin_dashboard.html')
        self.assertEqual(response.context['user'].user_type, 'super_admin')


    def test_other_user_dashboard_view(self):
        self.client.login(username='@jamescordon', password='Password123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.other_user)


    def test_get_society_dashboard(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('society_dashboard', args=[self.society.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'society/society_dashboard.html')
        self.assertIn('society', response.context)
        self.assertEqual(response.context['society'], self.society)
        session = self.client.session
        self.assertEqual(session['active_society_id'], self.society.id)


    def test_get_student_dashboard_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        session = self.client.session
        session['active_society_id'] = 1
        session.save()
        self.assertIn('active_society_id', self.client.session)
        response = self.client.get(reverse('to_student_dashboard'))
        self.assertNotIn('active_society_id', self.client.session)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


    def test_join_society_non_member(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        self.assertFalse(Membership.objects.filter(user=self.student, society=self.society2).exists())
        url = reverse('dashboard_from_mainpage', args=[self.society2.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': True, 'message': 'Successfully joined society.'})
        membership = Membership.objects.filter(user=self.student, society=self.society2)
        self.assertTrue(membership.exists())


    def test_join_society_already_a_member(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('dashboard_from_mainpage', args=[self.society.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(str(response.content, encoding='utf8'),{'success': False, 'error': 'You are already a member of this society.'})
