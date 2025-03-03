from django import forms
from social_media.models.university import University

class UniversityCreationForm(forms.ModelForm):
    """Form for users to request addition of a university into the hive."""
    #TODO: anyone can request for university to be registered as part of the hive
    class Meta:
        model = University
        fields = ["name", "domain", "logo"]


