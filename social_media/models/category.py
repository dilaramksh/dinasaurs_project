from django.core.validators import RegexValidator
from django.db import models

class Category(models.Model):
    """Model used for categories of societies present at universities"""

    name = models.CharField(max_length=30, choices=[('cultural', 'Cultural'), ('academic_career', 'Academic and Career'), ('faith', 'Faith'), ('political', 'Political'), ('sports', 'Sports'), ('volunteering', 'Volunteering'), ('other', 'Other')])

    def __str__(self):
        return self.name