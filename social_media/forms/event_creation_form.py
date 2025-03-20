from django import forms
from social_media.models.event import Event

class EventCreationForm(forms.ModelForm):
    """Form for students to create new events within a society."""

    picture = forms.ImageField(required=False)
    
    class Meta:
        model = Event
        fields = ["name", "description", "date", "location", "picture"]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }