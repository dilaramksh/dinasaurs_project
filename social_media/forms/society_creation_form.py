from django import forms
from social_media.models.society import Society

class SocietyCreationForm(forms.ModelForm):
    """Form for students to request to create societies."""
    #TODO: society president assigns roles after soc is created
    #TODO: set price and paid after soc is created
    # should have another path?

    logo = forms.ImageField(required=False)

    class Meta:
        model = Society
        fields = ["name", "society_email", "description", "category", "logo"]


