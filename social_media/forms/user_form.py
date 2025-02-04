from django import forms
from social_media.models import User

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']