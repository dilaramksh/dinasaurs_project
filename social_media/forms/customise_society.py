from django import forms
from social_media.models.society import Society

class customisationForm(forms.ModelForm):
    """Form for students to request to create societies."""
   
    class Meta:
        model = Society
        fields = ["name", "society_email", "description", "category", "price", "colour1", "colour2"]


