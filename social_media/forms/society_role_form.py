from django import forms
from social_media.models import SocietyRole

class SocietyRoleForm(forms.ModelForm):
    """
    Form for creating or editing society roles.

    This form allows users to input the name of a new role within a society.

    Attributes:
        role_name (CharField): The name of the role.
    """
    class Meta:
        model = SocietyRole
        fields = ['role_name']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new role name'}),
        }

class DeleteRoleForm(forms.Form):
    """
    Form for deleting a society role.

    This form allows users to select a role to delete from a dropdown list.
    The list excludes the roles of 'president' and 'member'.

    Attributes:
        role (ModelChoiceField): A dropdown field for selecting a role to delete.
    """
    role = forms.ModelChoiceField(
        queryset=SocietyRole.objects.none(), 
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Select Role to Delete"
    )

    def __init__(self, *args, **kwargs):
            society = kwargs.pop('society', None)
            super().__init__(*args, **kwargs)
            if society:
                self.fields['role'].queryset = (
                    SocietyRole.objects
                    .filter(society=society)
                    .exclude(role_name__iexact="president")
                    .exclude(role_name__iexact="member")
                )
