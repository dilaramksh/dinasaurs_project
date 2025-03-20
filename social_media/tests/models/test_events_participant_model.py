from django.test import TestCase
from django.db.utils import IntegrityError
from social_media.models import Event, Membership, EventsParticipant, Society, Category, User, University, SocietyRole
from django.utils.timezone import now

class EventsParticipantModelTest(TestCase):
    """Test cases for the EventsParticipant model."""

    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(name="Test University")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            user_type="student",
            university=self.university,
            start_date=now().date(),
            end_date=now().date()
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
        # Adjust the fields according to the actual SocietyRole model
        self.society_role = SocietyRole.objects.create(role_name="Member")
        self.membership = Membership.objects.create(
            user=self.user,
            society=self.society,
            society_role=self.society_role
        )
        self.events_participant = EventsParticipant.objects.create(
            event=self.event,
            membership=self.membership
        )

    def test_events_participant_creation(self):
        """Test if an EventsParticipant instance is correctly created."""
        self.assertEqual(self.events_participant.event, self.event)
        self.assertEqual(self.events_participant.membership, self.membership)

    def test_unique_events_participant_constraint(self):
        """Test the unique constraint on event and membership fields."""
        with self.assertRaises(IntegrityError):
            EventsParticipant.objects.create(
                event=self.event,
                membership=self.membership
            )

    def test_events_participant_str_representation(self):
        """Test the string representation of an EventsParticipant instance."""
        expected_str = f"{self.membership.user.username} - {self.event.name}"
        self.assertEqual(str(self.events_participant), expected_str)

    def test_events_participant_retrieval(self):
        """Test if the EventsParticipant instance can be retrieved from the database."""
        retrieved_participant = EventsParticipant.objects.get(id=self.events_participant.id)
        self.assertEqual(retrieved_participant, self.events_participant)

    def test_events_participant_deletion(self):
        """Test if an EventsParticipant instance is successfully deleted."""
        participant_id = self.events_participant.id
        self.events_participant.delete()
        with self.assertRaises(EventsParticipant.DoesNotExist):
            EventsParticipant.objects.get(id=participant_id)