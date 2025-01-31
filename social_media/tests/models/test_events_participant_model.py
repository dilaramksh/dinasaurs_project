from django.test import TestCase
from django.test import TestCase
from social_media.models import Category, Society, Event, User, Membership, SocietyRole, EventsParticipant
from django.core.exceptions import ValidationError
from django.test import TestCase
from datetime import date, timedelta

class EventsParticipantModelTestCase(TestCase):
    """Unit tests for the Events Participant Model"""

    fixtures = [
        'social_media/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
            description="A desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="pending",
        )
        self.event = Event.objects.create(
            name = "Test Event",
            society =  self.society,
            description =  "Our test desc!",
            date =  date.today() + timedelta(days=1),
            location =  "Here",
            )
        
        self.user = User.objects.get(email="john.doe@test.ac.uk")
        self.society_role = SocietyRole.objects.create(society=self.society, role_name="MyRole")
        self.membership = Membership.objects.create(user=self.user, society_role=self.society_role)
        
    def test_create_event_participant(self):
        events_parti = EventsParticipant(event=self.event, membership=self.membership)
        events_parti.full_clean()
        events_parti.save()
        self.assertEqual(EventsParticipant.objects.count(), 1)
    
    def test_unique_event_participant(self):
        EventsParticipant.objects.create(event=self.event, membership=self.membership)
        duplicate = EventsParticipant(event=self.event, membership=self.membership)
        with self.assertRaises(ValidationError):
            duplicate.full_clean()