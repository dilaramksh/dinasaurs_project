from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from datetime import date
from libgravatar import Gravatar
from .university import University  
import hashlib

DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

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
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True, default=DEFAULT_PROFILE_PICTURE)
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email

        if self.pk:
            old_instance = User.objects.get(pk=self.pk)
            if old_instance.profile_picture != self.profile_picture:
                old_instance.delete_old_picture()

        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()
        super().save(*args, **kwargs)
    

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def delete_old_picture(self):
        """Deletes the old profile picture from S3 if it's not the default"""
        if self.profile_picture and self.profile_picture.name != DEFAULT_PROFILE_PICTURE:
            default_storage.delete(self.profile_picture.name)




    def save(self, *args, **kwargs):
        """Handles deleting old profile pictures before saving a new one"""
        if self.pk:  # Check if instance exists
            old_instance = User.objects.get(pk=self.pk)
            if old_instance.profile_picture != self.profile_picture:
                old_instance.delete_old_picture()
        super().save(*args, **kwargs)
    

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'

