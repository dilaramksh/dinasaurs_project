from django import forms
from social_media.models import User, University


DEFAULT_PROFILE_PICTURE = "profile_pictures/default.jpg"

class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    profile_picture = forms.ImageField(required=False)
    email = forms.EmailField(disabled=True) 
    university = forms.ModelChoiceField(queryset=University.objects.all(), disabled=True)
    start_date = forms.DateField(disabled=True)
    end_date = forms.DateField(disabled=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'university','start_date', 'end_date', 'profile_picture']
    
 
        

