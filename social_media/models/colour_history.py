from django.db import models
from django.utils.timezone import now

class SocietyColorHistory(models.Model):
    society = models.ForeignKey('Society', on_delete=models.CASCADE, related_name='color_history')
    previous_colour1 = models.CharField(max_length=7)  
    previous_colour2 = models.CharField(max_length=7)
    updated_at = models.DateTimeField(default=now)  
    def __str__(self):
        return f"{self.society.name} Colors: {self.previous_colour1}, {self.previous_colour2} at {self.updated_at}"
