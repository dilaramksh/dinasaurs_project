from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from .society import Society

class Event(models.Model):
    """Model used for events in the societies"""

    name = models.CharField(max_length=250, blank=False)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    date = models.DateField(blank=False) 
    location = models.CharField(max_length=250, blank=False)

    def save(self, *args, **kwargs):
        """Ensure that the event date is in the future and the society is approved before saving."""
        if self.date < now().date():
            raise ValidationError({'date': 'The event date must be in the future.'})

        if not self.society:  
            raise ValidationError("Cannot save an event without an associated society.")

        if self.society.status != "approved":
            raise ValidationError("Cannot create an event for a non-approved society.")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
