from django.test import TestCase
from social_media.models import Category, Society, Event, User
from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date, timedelta

class EventModelTestCase(TestCase):
    """Unit tests for the Event Model"""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
            founder = User.objects.get(email="john.doe@test.ac.uk"),
            description="A desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="pending",
        )
        self.valid_event_data = {
            "name": "Test Event",
            "society": self.society,
            "description": "Our test desc!",
            "date": date.today() + timedelta(days=1),
            "location": "Here",
        }

    def test_create_valid_event(self):
        """Test creating an event with valid data."""
        event = Event(**self.valid_event_data)
        event.full_clean() 
        event.save()
        self.assertEqual(Event.objects.count(), 1)

    def test_name_required(self):
        """Test empty name raises ValidationError."""
        data = dict(self.valid_event_data, name="")
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_long_description(self):
        """Test exceeding max length of 1000 raises ValidationError."""
        data = dict(self.valid_event_data, description="A" * 1001)
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()