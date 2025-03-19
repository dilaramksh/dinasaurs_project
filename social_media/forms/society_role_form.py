from django import forms
from social_media.models import SocietyRole

class SocietyRoleForm(forms.ModelForm):
    class Meta:
        model = SocietyRole
        fields = ['role_name']
        widgets = {
            'role_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new role name'}),
        }

class DeleteRoleForm(forms.Form):
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
