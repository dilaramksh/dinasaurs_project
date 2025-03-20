from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now

DEFAULT_PICTURE = "events_picture/default.jpg"
from .society import Society

class Event(models.Model):
    """
    Model used for events in the societies.

    This model represents an event organized by a society. It includes details such as
    the event's name, description, date, location, and an optional picture.

    Attributes:
        name (CharField): The name of the event.
        society (ForeignKey): A reference to the society organising the event.
        description (CharField): A brief description of the event.
        date (DateField): The date of the event.
        location (CharField): The location where the event will be held.
        picture (ImageField): An optional field for uploading an event picture.
    """
    name = models.CharField(max_length=250, blank=False)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    date = models.DateField(blank=False) 
    location = models.CharField(max_length=250, blank=False)
    picture = models.ImageField(upload_to="events_picture/", blank=True, null=True, default=DEFAULT_PICTURE)

    def save(self, *args, **kwargs):
        """
        Ensure that the event date is in the future and the society is approved before saving.

        Raises:
            ValidationError: If the event date is in the past, the society is not associated,
                             or the society is not approved.
        """
        if self.date < now().date():
            raise ValidationError({'date': 'The event date must be in the future.'})

        if not self.society:  
            raise ValidationError("Cannot save an event without an associated society.")

        if self.society.status != "approved":
            raise ValidationError("Cannot create an event for a non-approved society.")


        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
