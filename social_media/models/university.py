from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class University(models.Model):
    """Model used for user authentication, and team member related information."""

    name = models.CharField(max_length=250, unique=True)
    domain = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}\.ac\.uk$',
            message="Domain must start with '@', followed by at least three alphanumerics, and end with '.ac.uk'."
        )]
    )

    # class Meta:
    #     """Model options."""

    #     ordering = ['last_name', 'first_name']

    # def full_name(self):
    #     """Return a string containing the user's full name."""

    #     return f'{self.first_name} {self.last_name}'

    # def gravatar(self, size=120):
    #     """Return a URL to the user's gravatar."""

    #     gravatar_object = Gravatar(self.email)
    #     gravatar_url = gravatar_object.get_image(size=size, default='mp')
    #     return gravatar_url

    # def mini_gravatar(self):
    #     """Return a URL to a miniature version of the user's gravatar."""
        
    #     return self.gravatar(size=60)