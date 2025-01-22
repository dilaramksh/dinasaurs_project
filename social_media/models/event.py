from django.db import models

from .society import Society

class Events(models.Model):
    """Model used for events in the societies"""

    name = models.CharField(max_length=250, blank=False)
    society_id = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    date = models.DateField(blank=False) 
    location = models.CharField(max_length=250, blank=False)

