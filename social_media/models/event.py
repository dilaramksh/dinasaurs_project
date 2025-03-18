from django.db import models
from .society import Society
from django.core.exceptions import ValidationError
from django.utils.timezone import now

DEFAULT_PICTURE = "events_picture/default.jpg"

class Event(models.Model):
    """Model used for events in the societies"""

    name = models.CharField(max_length=250, blank=False)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    date = models.DateField(blank=False) 
    location = models.CharField(max_length=250, blank=False)
    picture = models.ImageField(upload_to="event_picture/", blank=True, null=True, default=DEFAULT_PICTURE)

    # ensure date is in the future
    #clean() is called automatically when Django validates the model
    def clean(self):
        """Ensure that the event date is in the future."""
        if self.date < now().date():
            raise ValidationError({'date': 'The event date must be in the future.'})
         
        if self.society.status != "approved":
            raise ValidationError("Cannot create an event for a non-approved society.")

    def __str__(self):
        return self.name  
