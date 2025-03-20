from django.test import TestCase
from django.core.exceptions import ValidationError
from social_media.forms import EventCreationForm
from social_media.models import Event, Society, User
from datetime import date, timedelta

class EventCreationFormTest(TestCase):
    def setUp(self):
        """Set up test data for all test methods."""
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
        """Ensure the form is valid when all required fields are provided."""
        form_data = {
            'name': 'Test Event',
            'society': self.society.id,  
            'description': 'A detailed event description',
            'date': date.today() + timedelta(days=30),
            'location': 'Main Campus Hall'
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")

    def test_form_invalid_with_past_date(self):
        """Ensure the form is invalid when the event date is in the past."""
        form_data = {
            'name': 'Past Event',
            'society': self.society.id,
            'description': 'An event with a past date',
            'date': date.today() - timedelta(days=1),
            'location': 'Old Location'
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_form_invalid_without_society(self):
        """Ensure the form is invalid when the required 'society' field is missing."""
        form_data = {
            'name': 'No Society Event',
            'description': 'An event without a society',
            'date': date.today() + timedelta(days=15),
            'location': 'Somewhere'
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('society', form.errors)

    def test_form_invalid_without_location(self):
        """Ensure the form is invalid when the required 'location' field is missing."""
        form_data = {
            'name': 'No Location Event',
            'society': self.society.id,
            'description': 'An event without a location',
            'date': date.today() + timedelta(days=15),
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)

    def test_form_invalid_with_empty_description(self):
        """Ensure the form is invalid when description is empty."""
        form_data = {
            'name': 'Empty Description Event',
            'society': self.society.id,
            'description': '',
            'date': date.today() + timedelta(days=10),
            'location': 'Main Hall'
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_form_invalid_with_long_name(self):
        """Ensure the form rejects names longer than allowed."""
        form_data = {
            'name': 'X' * 300,
            'society': self.society.id,
            'description': 'Valid description',
            'date': date.today() + timedelta(days=10),
            'location': 'Main Hall'
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_invalid_with_long_location(self):
        """Ensure the form rejects location names that are too long."""
        form_data = {
            'name': 'Valid Event Name',
            'society': self.society.id,
            'description': 'Valid description',
            'date': date.today() + timedelta(days=10),
            'location': 'X' * 300  
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)

    def test_form_widget_customization(self):
        """Ensure the 'date' field has the correct DateInput widget."""
        form = EventCreationForm()
        self.assertEqual(
            form.fields['date'].widget.attrs['type'], 'date'
        )
        self.assertEqual(
            form.fields['date'].widget.attrs['class'], 'form-control'
        )

    def test_form_field_choices(self):
        """Ensure all expected fields are present in the form."""
        form = EventCreationForm()
        expected_fields = ['name', 'description', 'date', 'location']
        for field in expected_fields:
            self.assertIn(field, form.fields)

