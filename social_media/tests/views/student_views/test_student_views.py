
from django.test import TestCase
from django.urls import reverse
from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import *
from django.contrib.messages import get_messages


class StudentViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")

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

        self.user2 = User.objects.create_user(
            first_name='john',
            last_name='smit',
            email='johnsmith@kcl.ac.uk',
            user_type='student',
            university=university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@johnsmith',
            password='Password123'
        )

        self.category = Category.objects.create(
            name='sports'
        )

        self.society = Society.objects.create(
            name='basketballclub',
            status='approved',
            founder=self.user,
            society_email='basketballclub@kcl.ac.uk',
            description='basketball club',
            category=self.category,
            paid_membership=False,
            colour1='#FFFFFF',
            colour2='#FFFFFF'
        )

        self.role = SocietyRole.objects.create(
            society=self.society,
            role_name='president'
        )

        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.role
        )

        self.valid_form_data = {
            'name':'Baseballclub',
            'society_email':'baseball@kcl.ac.uk',
            'description':'baseball club',
            'category':self.category.id
        }

        self.invalid_form_data = {
            'name': '',
            'society_email': 'footballclub@kcl.ac.uk',
            'description': 'football club',
            'category': self.category.id
        }


    # PASSES
    def test_help_page_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/help')

    # PASSES
    def test_society_browser_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('society_browser'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('student/society_browser.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')

    # PASSES
    def test_valid_society_creation_request_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.valid_form_data)
        self.assertEqual(Society.objects.count(), 2)
        created_society = Society.objects.exclude(id=self.society.id).first()
        self.assertEqual(created_society.status, "pending")
        self.assertEqual(created_society.founder, self.user)
        self.assertEqual(created_society.name, self.valid_form_data['name'])
        self.assertEqual(created_society.society_email, self.valid_form_data['society_email'])
        self.assertEqual(created_society.description, self.valid_form_data['description'])
        self.assertEqual(created_society.category, self.category)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your society request has been submitted for approval.")
        self.assertRedirects(response, reverse('dashboard'))

    # PASSES
    def test_invalid_society_creation_request_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.invalid_form_data)
        self.assertEqual(Society.objects.count(), 1)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "There was an error with your request submission. Please try again.")

    # PASSES
    def test_else_society_creation_form(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.get(reverse('society_creation_request'))
        self.assertTemplateUsed(response, 'student/submit_society_request.html')
        form = response.context['form']
        self.assertIsInstance(form, SocietyCreationForm)
        self.assertIn('form', response.context)

    # PASSES
    def test_no_filters_view_societies(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_societies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/view_societies.html')
        self.assertIn('societies', response.context)

    # PASSES
    def test_search_query_view_societies(self):
        response = self.client.get(reverse('view_societies'), {'search': 'basketballclub'})
        self.assertEqual(response.status_code, 200)
        societies = response.context['societies']
        self.assertEqual(len(societies), 1)
        self.assertIn(self.society, societies)

    # PASSES
    def test_category_filter_view_societies(self):
        response = self.client.get(reverse('view_societies'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        societies = response.context['societies']
        self.assertIn(self.society, societies)

    # PASSES
    def test_context_view_societies(self):
        response = self.client.get(reverse('view_societies'))
        self.assertIn('societies', response.context)
        self.assertIn('categories', response.context)
        self.assertIn('search_query', response.context)
        self.assertIn('selected_category', response.context)
        self.assertIn('society_posts', response.context)

    # PASSES
    def test_student_events_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('student_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_events.html')
        self.assertIn('student', response.context)
        self.assertIn('user_societies', response.context)
        self.assertIn('user_events', response.context)

    # PASSES
    def test_no_selected_society_student_societies_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('student_societies')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        user_societies = response.context['user_societies']
        self.assertIn(self.society, user_societies)
        self.assertIsNone(response.context['selected_society'])
        self.assertTemplateUsed(response, 'student/student_societies.html')

    # PASSES
    def test_selected_society_student_societies_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('student_societies')
        response = self.client.get(url, {'society_id': self.society.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['selected_society'], self.society)

    # PASSES
    def test_user_cannot_access_unrelated_society(self):
        self.client.login(username='@johnsmith', password='Password123')
        url = reverse('student_societies') + f'?society_id={self.society.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['selected_society'])
        self.assertNotIn(self.society, response.context['user_societies'])

    # PASSES
    def test_student_societies_committee_members(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('student_societies')
        response = self.client.get(url, {'society_id': self.society.id})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, response.context['committee_members'])


