from django import forms
from django.contrib.auth import authenticate
from social_media.models import User

class LogInForm(forms.Form):
    """Form for user login."""
    
    email_or_username = forms.CharField(label='Email / Username', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    def get_user(self):
        """Return the user object if the credentials are valid."""
        if not self.is_valid():
            return None

        identifier = self.cleaned_data['email_or_username']
        password = self.cleaned_data['password']
        
        """User can log in with username or email"""
        try:
            user = User.objects.get(email=identifier)
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                return None

        authenticated_user = authenticate(username=user.username, password=password)
        return authenticated_user


