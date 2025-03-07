from django.core.validators import RegexValidator
from django.db import models

class University(models.Model):
    """Model used for infromation of different universities"""

    name = models.CharField(max_length=250, unique=True)
    domain = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}\.ac\.uk$',
            message="Domain must start with '@', followed by at least three alphanumerics, and end with '.ac.uk'."
        )]
    )

    def __str__(self):
        return self.name
