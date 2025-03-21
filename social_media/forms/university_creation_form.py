from django import forms
from social_media.models.university import University

class UniversityCreationForm(forms.ModelForm):
    """
    Form for users to request the addition of a university into the hive.

    This form allows users to input details about the university such as name, domain,
    and an optional logo.

    Attributes:
        name (CharField): The name of the university.
        domain (CharField): The domain of the university.
        logo (ImageField): An optional field for uploading a university logo.
    """
    
    class Meta:
        model = University
        fields = ["name", "domain", "logo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = False 


