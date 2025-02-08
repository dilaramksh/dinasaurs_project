from django import forms
from django.contrib.auth import authenticate
from social_media.models import User

class LogInForm(forms.Form):
    """Form for user login."""
    
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    def get_user(self):
        """Return the user object if the credentials are valid."""
        if not self.is_valid():
            return None

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        try:
            user = User.objects.get(email=email)
            return authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            return None


