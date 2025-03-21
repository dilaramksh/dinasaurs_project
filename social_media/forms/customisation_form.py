from django import forms
from social_media.models.society import Society

class CustomisationForm(forms.ModelForm):
    """
    Form for students to customise the appearance of their societies.

    This form allows users to select two colors for their society's theme.
    The colors are selected using a color picker widget.

    Attributes:
        colour1 (CharField): The primary color for the society's theme.
        colour2 (CharField): The secondary color for the society's theme.
    """
    colour1 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        help_text="Select the primary color for your society."
    )
    colour2 = forms.CharField(
        widget=forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        help_text="Select the secondary color for your society."
    )

    class Meta:
        model = Society
        fields = ['colour1', 'colour2']
        help_texts = {
            'colour1': 'Select the primary color for your society.',
            'colour2': 'Select the secondary color for your society.',
        }