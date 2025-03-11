from django import forms
from social_media.models.society import Society

class CustomisationForm(forms.ModelForm):
    """Form for students to request to create societies."""
    colour1 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'})
    )
    colour2 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'})
    )

    class Meta:
        model = Society
        fields = ['colour1', 'colour2']

    