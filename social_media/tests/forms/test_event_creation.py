'''
from django.test import TestCase
from django.core.exceptions import ValidationError
from social_media.forms import EventCreationForm
from social_media.models import Event, Society, User
from datetime import date, timedelta

class EventCreationFormTest(TestCase):
    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        """

        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass123'
        )
        
        self.society = Society.objects.create(
            name='Test Society',
            description='A test society',
            creator=self.user
        )

    def test_form_valid_with_all_required_fields(self):
        """
        Test that the form is valid when all required fields are provided correctly.
        """
        form_data = {
            'name': 'Test Event',
            'society': self.society,
            'description': 'A detailed event description',
            'date': date.today() + timedelta(days=30),
            'location': 'Main Campus Hall'
        }
        
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), 
                        f"Form errors: {form.errors}")

    def test_form_invalid_with_past_date(self):
        """
        Test that the form is invalid when the event date is in the past.
        """
        form_data = {
            'name': 'Past Event',
            'society': self.society,
            'description': 'An event with a past date',
            'date': date.today() - timedelta(days=1),
            'location': 'Old Location'
        }
        
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_form_invalid_with_missing_fields(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form_data = {
            'name': 'Incomplete Event',
        }
        
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 1)

    def test_form_invalid_with_extremely_long_description(self):
        """
        Test form validation with an extremely long description.
        """
        form_data = {
            'name': 'Long Description Event',
            'society': self.society,
            'description': 'X' * 10001, 
            'date': date.today() + timedelta(days=30),
            'location': 'Long Description Hall'
        }
        
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_field_choices(self):
        """
        Test that the form fields are correctly mapped from the model.
        """
        form = EventCreationForm()
        
        expected_fields = ['name', 'society', 'description', 'date', 'location']
        for field in expected_fields:
            self.assertIn(field, form.fields)

'''