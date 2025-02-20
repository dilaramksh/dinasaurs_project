from django import forms
from social_media.models import User, University

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'university','start_date', 'end_date']

    email = forms.EmailField(disabled=True)
    university = forms.ModelChoiceField(queryset=University.objects.all(), disabled=True)
    start_date = forms.DateField(disabled=True)
    end_date = forms.DateField(disabled=True)