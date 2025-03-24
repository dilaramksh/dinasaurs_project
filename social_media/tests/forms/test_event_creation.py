from django.test import TestCase
from social_media.forms import EventCreationForm
from social_media.models import Event, Society, Category, University, User
from datetime import date
from django.core.exceptions import ValidationError
from django.utils.timezone import now, timedelta
from datetime import timedelta

class EventCreationFormTest(TestCase):
    """Test cases for the EventCreationForm."""

    def setUp(self):
        self.university = University.objects.create(
            name="King's College London 2",
            domain='@kcl2.ac.uk',
        )
        self.user = User.objects.create(
            first_name='jane',
            last_name='doe',
            email='janedoe@kcl.ac.uk',
            user_type='student',
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
            username='@janedoe',
        )

        category_name = 'sports'
        self.category, created = Category.objects.get_or_create(name=category_name)

        self.society = Society.objects.create(
            name= 'footballclub',
            founder=self.user,
            society_email='footballclub@kcl.ac.uk',
            description='football club',
            category=self.category,
            paid_membership=False,
            status = 'approved'
        )

    def test_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date': date.today(),
            'society': self.society,
            'location': 'Test Location'
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Test form with invalid data."""
        form_data = {
            'name': '',
            'description': 'This is a test event.',
            'date': 'invalid-date',
            'society': self.society,
            'location': 'Test Location',
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('date', form.errors)



    def test_form_missing_data(self):
        """Test form with missing data."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
        }
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertIn('location', form.errors)

    def test_form_empty_data(self):
        """Test form with empty data."""
        form_data = {}
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('description', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('location', form.errors)

    def test_form_optional_picture(self):
        """Test form with optional picture field."""
        form_data = {
            'name': 'Test Event',
            'description': 'This is a test event.',
            'date': date.today(),
            'society': self.society,
            'location': 'Test Location',
        }
        form = EventCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('picture', form.errors)

    def test_save_event_with_future_date(self):
        """Test saving an event with a future date should be successful."""
        event = Event(
            name="Future Event",
            society=self.society,
            description="An upcoming event.",
            date=now().date() + timedelta(days=5),
            location="Test Location"
        )
        event.save()
        self.assertIsNotNone(event.id)  # Ensure it was saved successfully
    
    def test_save_event_with_past_date_raises_error(self):
        """Test saving an event with a past date should raise ValidationError."""
        event = Event(
            name="Past Event",
            society=self.society,
            description="A past event.",
            date=now().date() - timedelta(days=5),
            location="Test Location"
        )
        with self.assertRaises(ValidationError) as context:
            event.save()
        self.assertIn('date', context.exception.message_dict)
    
    def test_form_rejects_past_event_date(self):
        """Test that the form raises a ValidationError when the event date is in the past."""
        form_data = {
            "name": "Past Event",
            "description": "An event that should fail validation.",
            "date": now().date() - timedelta(days=1),
            "society": self.society,
            "location": "Test Location",
        }
        form = EventCreationForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)
        self.assertEqual(form.errors["date"][0], "The event date cannot be in the past.")
    


    
    def test_form_date_in_the_past(self):
        """Test form rejects a date in the past."""
        past_date = date.today() - timedelta(days=1)
        form_data = {
            'name': 'Past Event',
            'description': 'Event in the past.',
            'date': past_date,
            'location': 'Old Location',
        }

        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)
        self.assertEqual(form.errors['date'], ['The event date cannot be in the past.'])
