from django.db import models
from django.core.exceptions import ValidationError

from .society import Society

class News(models.Model):
    """Model used for news in the society"""

    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    likes = models.IntegerField(default=0)

    
    def clean(self):
        # If society is not approved, forbid
        if self.society.status != "approved":
            raise ValidationError("Cannot create membership for a non-approved society.")