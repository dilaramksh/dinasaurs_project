from django.core.validators import RegexValidator
from django.db import models

class University(models.Model):
    """Model used for infromation of different universities"""

    name = models.CharField(max_length=250, unique=True)
    domain = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'\w{3,}\.ac\.uk$',
            message="Domain must contain at least three alphanumerics, and end with '.ac.uk'."
        )]
    )
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("blocked", "Blocked")], default="pending")
    logo = models.ImageField(upload_to="university_logos/", blank=True, null=True)

    def __str__(self):
        return self.name  
