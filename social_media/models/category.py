from django.core.validators import RegexValidator
from django.db import models

class Category(models.Model):
    """Model used for categories of societies present at universities"""

    name = models.CharField(max_length=50, blank=False)
