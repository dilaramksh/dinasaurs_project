from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError
from datetime import date
from libgravatar import Gravatar
from .university import University  


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must start with @ followed by at least three alphanumeric characters (letters, numbers, or underscore).'
        )],
        help_text='Enter a username starting with "@" followed by at least three alphanumeric characters.',
    )
    email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()])
    user_type = models.CharField(max_length=100, 
                                 choices=[('super_admin', 'Super Admin'), ('uni_admin', 'University Admin'), ('student', 'Student')], 
                                 default='student')
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    start_date= models.DateField(blank=False)
    end_date = models.DateField(blank=False)
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.username:  # Automatically set username to email if not provided
            self.username = self.email
        super().save(*args, **kwargs)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)