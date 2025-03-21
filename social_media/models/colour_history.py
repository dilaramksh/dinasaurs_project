from django.db import models
from django.utils.timezone import now

class SocietyColorHistory(models.Model):
    """
    Model to store the history of color changes for a society.

    This model keeps track of the previous colors used by a society and the date
    when the colors were updated.

    Attributes:
        society (ForeignKey): A reference to the society whose color history is being tracked.
        previous_colour1 (CharField): The previous primary color of the society.
        previous_colour2 (CharField): The previous secondary color of the society.
        updated_at (DateTimeField): The date and time when the colors were updated.
    """
    society = models.ForeignKey('Society', on_delete=models.CASCADE, related_name='color_history')
    previous_colour1 = models.CharField(max_length=7)  
    previous_colour2 = models.CharField(max_length=7)
    updated_at = models.DateTimeField(default=now)  
    def __str__(self):
        return f"{self.society.name} Colors: {self.previous_colour1}, {self.previous_colour2} at {self.updated_at}"
