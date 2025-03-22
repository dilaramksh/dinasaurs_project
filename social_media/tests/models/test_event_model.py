from django.test import TestCase
from django.core.exceptions import ValidationError

from django.utils.timezone import now
from datetime import timedelta
from social_media.models import Event, Society, Category, User, University

class EventModelTest(TestCase):
    """Test cases for the Event model."""

    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(
            name="Test University",
            domain='test.ac.uk',
        )

        self.user = User.objects.create_user(
            username="@testuser",
            password="testpass",
            email="testuser@test.ac.uk",
            first_name="Test",
            last_name="User",
            user_type="student",
            university=self.university,
            start_date='2023-09-23',
            end_date='2026-05-06',
        )
        self.category = Category.objects.create(name="Test Category")
        self.society = Society.objects.create(
            name="Test Society",
            founder=self.user,
            society_email="test@society.com",
            description="A test society",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="approved"
        )
        self.event = Event.objects.create(
            name="Test Event",
            society=self.society,
            description="This is a test event.",
            date=now().date(),
            location="Test Location"
        )

    def test_event_creation(self):
        """Test if an Event instance is correctly created."""
        self.assertEqual(self.event.name, "Test Event")
        self.assertEqual(self.event.society, self.society)
        self.assertEqual(self.event.description, "This is a test event.")
        self.assertEqual(self.event.date, now().date())
        self.assertEqual(self.event.location, "Test Location")
        self.assertEqual(self.event.picture, "events_picture/default.jpg")

    def test_event_str_representation(self):
        """Test the string representation of an Event instance."""
        self.assertEqual(str(self.event), "Test Event")

    def test_event_date_in_future(self):
        """Test that the event date must be in the future."""
        self.event.date = now().date() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            self.event.save()
    
    def test_event_for_non_approved_society(self):
        """Test that an event cannot be created for a non-approved society."""
        self.society.status = "pending"
        self.society.save()
        event = Event(
            name="Test Event",
            society=self.society,
            description="This is a test event.",
            date=now().date(),
            location="Test Location"
        )
        with self.assertRaises(ValidationError):
            event.save()