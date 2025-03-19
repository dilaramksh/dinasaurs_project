from lib2to3.fixes.fix_input import context

from django.test import TestCase
from django.urls import reverse

from social_media.forms.society_creation_form import SocietyCreationForm
from social_media.models import *
from django.contrib.messages import get_messages


class StudentViewTestCase(TestCase):

    def setUp(self):
        university = University.objects.create(name="King's College London")
        self.category = Category.objects.get_or_create(name='sports')

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

        self.category = Category.objects.create(
            name='sports'
        )

        self.valid_form_data = {
            'name':'Basketballclub',
            'society_email':'basketballclub@kcl.ac.uk',
            'description':'basketball club',
            'category':self.category.id
        }

        self.invalid_form_data = {
            'name': '',
            'society_email': 'basketballclub@kcl.ac.uk',
            'description': 'basketball club',
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
        self.assertEqual(Society.objects.count(), 1)
        created_society = Society.objects.first()
        self.assertEqual(created_society.name, self.valid_form_data['name'])
        self.assertEqual(created_society.society_email, self.valid_form_data['society_email'])
        self.assertEqual(created_society.description, self.valid_form_data['description'])
        self.assertEqual(created_society.category.name, Category.objects.get(id=self.valid_form_data['category']).name)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Your society request has been submitted for approval.")
        self.assertRedirects(response, reverse('dashboard'))


    # PASSES
    def test_invalid_society_creation_request_view(self):
        self.client.login(username='@janedoe', password='Password123')
        url = reverse('society_creation_request')
        response = self.client.post(url, data=self.invalid_form_data)
        self.assertEqual(Society.objects.count(), 0)
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




    # FAILING
    def test_view_societies_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('view_societies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/view_societies.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')

        context = response.context
        self.assertIn('societies', context)
        self.assertIn('search_query', context)
        self.assertIn('selected_category', context)
        self.assertIn('categories', context)


        response_with_search = self.client.get(reverse('view_societies') + '?search=basketball')
        self.assertEqual(response_with_search.status_code, 200)
        self.assertIn('societies', response_with_search.context)

        #  FAILING
        category = Category.objects.create(name="sports")
        response_with_category = self.client.get(reverse('view_societies') + f'?category={category.id}')
        self.assertEqual(response_with_category.status_code, 200)
        self.assertIn('societies', response_with_category.context)
        self.assertTrue(response_with_category.context['societies'].filter(category=category).exists())

    def test_student_societies_view(self):
        # Log in the user
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)

        # Test with no societies (empty `user_societies`)
        self.user_societies = []  # Simulate a user with no societies
        response = self.client.get(reverse('student_societies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_societies.html')

        # Check that no societies are listed
        context = response.context
        self.assertIn('student', context)
        self.assertIn('user_societies', context)
        self.assertIn('selected_society', context)
        self.assertIn('society_roles', context)
        self.assertEqual(context['user_societies'], [])
        self.assertEqual(context['society_roles'].count(), 0)

        invalid_society_id = 999999
        response_invalid_society = self.client.get(reverse('student_societies') + f'?society_id={invalid_society_id}')
        self.assertEqual(response_invalid_society.status_code, 200)
        context_invalid_society = response_invalid_society.context
        self.assertIsNone(context_invalid_society['selected_society'])

        if self.user_societies:
            valid_society_id = self.user_societies[0].id
            response_valid_society = self.client.get(reverse('student_societies') + f'?society_id={valid_society_id}')
            self.assertEqual(response_valid_society.status_code, 200)
            context_valid_society = response_valid_society.context
            self.assertEqual(context_valid_society['selected_society'].id, valid_society_id)


        context = response.context
        self.assertIn('student', context)
        self.assertIn('user_societies', context)
        self.assertIn('selected_society', context)
        self.assertIn('society_roles', context)



    def test_student_events_view(self):
        login_success = self.client.login(username='@janedoe', password='Password123')
        self.assertTrue(login_success)
        response = self.client.get(reverse('student_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_events.html')
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'].user_type, 'student')

        context = response.context
        self.assertIn('student', context)
        self.assertIn('user_societies', context)
        self.assertIn('user_events', context)



