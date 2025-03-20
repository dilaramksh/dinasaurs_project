from django.core.validators import RegexValidator
from django.db import models
from .event import Event
from .membership import Membership

class EventsParticipant(models.Model):
    """
    Model used for recording participants of an event.

    This model represents the relationship between an event and its participants.
    Each participant is associated with a membership.

    Attributes:
        event (ForeignKey): A reference to the event the participant is attending.
        membership (ForeignKey): A reference to the membership of the participant.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)

    class Meta:
        """Member cannot be recorded as a participant of an event more than once."""
        constraints = [
            models.UniqueConstraint(fields=["event", "membership"], name="unique_events_participant")
        ]
   