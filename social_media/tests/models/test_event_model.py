from django.test import TestCase
from social_media.models import Category, Society, Event, User
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class EventModelTestCase(TestCase):
    """Unit tests for the Event Model"""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
            founder=User.objects.get(email="john.doe@test.ac.uk"),
            description="A desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="approved",
        )
        self.pending_society = Society.objects.create(
            name="Pending Soc",
            society_email="pending@test.ac.uk",
            founder=User.objects.get(email="john.doe@test.ac.uk"),
            description="Pending desc.",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFFFFF",
            colour2="#000000",
            termination_reason=None,
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
        """Test that an empty name raises ValidationError."""
        data = dict(self.valid_event_data, name="")
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_long_description(self):
        """Test that exceeding max length of 1000 raises ValidationError."""
        data = dict(self.valid_event_data, description="A" * 1001)
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_event_date_must_be_future(self):
        """Test that past dates raise ValidationError."""
        data = dict(self.valid_event_data, date=date.today() - timedelta(days=1))
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_cannot_create_event_for_non_approved_society(self):
        """Test that creating an event for a non-approved society raises ValidationError."""
        data = dict(self.valid_event_data, society=self.pending_society)
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_location_required(self):
        """Test that an empty location raises ValidationError."""
        data = dict(self.valid_event_data, location="")
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_max_length_constraints(self):
        """Test that exceeding max length constraints raises ValidationError."""
        data = dict(self.valid_event_data, name="A" * 251)
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()

        data = dict(self.valid_event_data, location="A" * 251)
        event = Event(**data)
        with self.assertRaises(ValidationError):
            event.full_clean()
