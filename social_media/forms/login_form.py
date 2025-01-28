from django import forms
from django.contrib.auth import authenticate

class LogInForm(forms.Form):
    """Form for user login."""
    
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    def get_user(self):
        """Return the user object if the credentials are valid."""
        user = None
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)
        return user