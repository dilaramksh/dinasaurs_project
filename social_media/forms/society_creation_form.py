from django import forms
from social_media.models.society import Society

class SocietyCreationForm(forms.ModelForm):
    """
    Form for students to request to create societies.

    This form allows users to input details about the society such as name, email,
    description, category, and an optional logo.

    Attributes:
        logo (ImageField): An optional field for uploading a society logo.
    """
    logo = forms.ImageField(required=False)

    class Meta:
        model = Society
        fields = ["name", "society_email", "description", "category", "logo"]


