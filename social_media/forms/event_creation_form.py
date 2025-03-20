from django import forms
from django.utils import timezone
from social_media.models.event import Event

class EventCreationForm(forms.ModelForm):
    """
    Form for students to create new events within a society.

    This form allows users to input details about the event such as name, description,
    date, location, and an optional picture. It ensures that the event date is not in the past.

    Attributes:
        picture (ImageField): An optional field for uploading an event picture.
    """

    picture = forms.ImageField(required=False)

    class Meta:
        model = Event
        fields = ["name", "description", "date", "location", "picture"]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_date(self):
        """
        Ensure the event date is today or in the future.

        Raises:
            forms.ValidationError: If the event date is in the past.

        Returns:
            date: The cleaned event date.
        """
        event_date = self.cleaned_data.get("date")
        if event_date and event_date < timezone.localdate():
            raise forms.ValidationError("The event date cannot be in the past.")
        return event_date