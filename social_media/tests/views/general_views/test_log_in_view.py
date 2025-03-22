from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from social_media.forms import LogInForm
from social_media.models import User
from social_media.tests.helpers import LogInTester, MenuTesterMixin, reverse_with_next

class LogInViewTestCase(TestCase, LogInTester, MenuTesterMixin):
    """Tests of the log in view."""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.login_url = reverse('log_in')
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.login_url,'/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_no_menu(response)

    def test_get_log_in_with_redirect(self):
        destination_url = reverse('profile')
        self.login_url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    
    def test_get_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.login_url, follow=True)
        self.redirect_url = reverse('dashboard')
        self.assertRedirects(response, self.redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')


    def test_unsuccesful_log_in_wrong_password(self):
        form_input = { 'email_or_username': '@johndoe', 'password': 'WrongPassword123' }
        response = self.client.post(self.login_url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)
    
    def test_log_in_with_blank_form(self):
        """Test submitting a completely blank login form."""
        form_input = {}  
        response = self.client.post(self.login_url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound) 
        self.assertFalse(self._is_logged_in())  
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_username(self):
        form_input = { 'email_or_username': '', 'password': 'Password123' }
        response = self.client.post(self.login_url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_log_in_with_blank_password(self):
        form_input = { 'email_or_username': '@johndoe', 'password': '' }
        response = self.client.post(self.login_url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'general/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_succesful_log_in(self):
        form_input = { 'email_or_username': '@johndoe', 'password': 'Password123' }
        response = self.client.post(self.login_url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assert_menu(response)

    def test_succesful_log_in_with_redirect(self):
        redirect_url = reverse('profile')
        form_input = { 'email_or_username': '@johndoe', 'password': 'Password123', 'next': redirect_url }
        response = self.client.post(self.login_url, form_input, follow=True)
        
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'general/profile.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_post_log_in_redirects_when_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        form_input = { 'username': '@wronguser', 'password': 'WrongPassword123' }
        response = self.client.post(self.login_url, form_input, follow=True)
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')

    def test_post_log_in_with_incorrect_credentials_and_redirect(self):
        redirect_url = reverse('profile')
        form_input = { 'email_or_username': '@johndoe', 'password': 'WrongPassword123', 'next': redirect_url }
        response = self.client.post(self.login_url, form_input)
        next = response.context['next']
        self.assertEqual(next, redirect_url)


