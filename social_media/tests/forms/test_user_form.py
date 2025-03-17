"""Unit tests of the user form."""
from django import forms
from django.test import TestCase
from social_media.forms import UserForm
from social_media.models import User, University
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date



class UserFormTestCase(TestCase):
    """Unit tests of the user form."""

    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.university = University.objects.get(pk=1)

        self.form_input = {
            'first_name': 'UName',
            'last_name': 'ULName',
            'username': '@updatedusername'
        }

        self.image = SimpleUploadedFile(
            "profile.jpg", 
            content=b"image content", 
            content_type="image/jpeg"
        )

    def test_form_has_necessary_fields(self):
        form = UserForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def test_valid_user_form(self):
        form = UserForm(data=self.form_input, instance=self.user)  # Pass instance
        if not form.is_valid():
            print(form.errors)  # Debugging: Print errors if form fails
        self.assertTrue(form.is_valid())


    def test_form_uses_model_validation(self):
        self.form_input['username'] = 'badusername'
        form = UserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_empty_name_field(self):
        # Test empty first_name or last_name fields
        form_data = self.form_input.copy()
        form_data['first_name'] = ''
        form_data['last_name'] = ''
        form = UserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)

    def test_profile_picture_optional_field(self):
        form_data = self.form_input.copy()
        form_data['profile_picture'] = self.image
        form = UserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        form_data['profile_picture'] = None
        form = UserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_disabled_fields(self):
        form = UserForm(data=self.form_input, instance=self.user)
        
        self.assertTrue(form.fields['email'].disabled)
        self.assertTrue(form.fields['university'].disabled)
        self.assertTrue(form.fields['start_date'].disabled)
        self.assertTrue(form.fields['end_date'].disabled)

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = UserForm(instance=user, data=self.form_input)
        before_count = User.objects.count()
        form.save()
        user.refresh_from_db
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(user.username, '@updatedusername')
        self.assertEqual(user.first_name, 'UName')
        self.assertEqual(user.last_name, 'ULName')
        self.assertEqual(user.email, 'john.doe@test.ac.uk')
        self.assertEqual(user.university, self.university)
        self.assertEqual(user.start_date, date(2025, 1, 1))
        self.assertEqual(user.end_date, date(2026, 1, 1))

    def test_save_form_with_profile_picture(self):
        form_data = self.form_input.copy()
        form_data['profile_picture'] = self.image
        form = UserForm(data=form_data, instance=self.user)

        if form.is_valid():
            updated_user = form.save(commit=False)  
            updated_user.profile_picture = self.image  
            updated_user.save() 

            self.assertTrue(updated_user.profile_picture) 
            self.assertNotEqual(updated_user.profile_picture.name, 'profile_pictures/default.jpg') 
