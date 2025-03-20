from django import forms
from django.utils import timezone
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

    def clean_date(self):
        """Ensure the event date is today or in the future."""
        event_date = self.cleaned_data.get("date")
        if event_date and event_date < timezone.localdate():  # Use timezone.localdate() instead of now().date()
            raise forms.ValidationError("The event date cannot be in the past.")
        return event_date