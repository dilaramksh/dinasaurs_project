from django import forms
from django.test import TestCase
from social_media.forms import LogInForm
from social_media.models import User

class LogInFormTestCase(TestCase):
    """Unit tests for the log in form."""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = {'email_or_username': '@janedoe', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = LogInForm()
        self.assertIn('email_or_username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username_or_email(self):
        self.form_input['email_or_username'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_user_does_not_exist(self):
        form_input = {
            "email_or_username": "nonexistentuser",
            "password": "testpassword"
        }
        form = LogInForm(data=form_input)
        self.assertTrue(form.is_valid())
        self.assertIsNone(form.get_user())

    def test_form_accepts_incorrect_username_or_email(self):
        self.form_input['email_or_username'] = 'ja'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = LogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_can_authenticate_valid_user_username(self):
        fixture = User.objects.get(username='@johndoe')
        form_input = {'email_or_username': '@johndoe', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)
    
    def test_can_authenticate_valid_user_email(self):
        fixture = User.objects.get(email='john.doe@test.ac.uk')
        form_input = {'email_or_username': 'john.doe@test.ac.uk', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, fixture)

    def test_invalid_credentials_do_not_authenticate(self):
        form_input = {'email_or_username': '@johndoe', 'password': 'WrongPassword123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_password_does_not_authenticate(self):
        form_input = {'email_or_username': '@johndoe', 'password': ''}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)

    def test_blank_username_does_not_authenticate(self):
        form_input = {'email_or_username': '', 'password': 'Password123'}
        form = LogInForm(data=form_input)
        user = form.get_user()
        self.assertEqual(user, None)
        
