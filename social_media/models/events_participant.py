from django.core.validators import RegexValidator
from django.db import models
from .event import Event

class EventsParticipant(models.Model):
    """Model used for recording participants of an event"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
