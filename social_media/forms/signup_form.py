from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from social_media.models import User, University
from social_media.mixins import NewPasswordMixin
from django.utils.timezone import now

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    start_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    end_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    university = forms.ModelChoiceField( 
        queryset=University.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select your university",
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def clean(self):
        """Ensure date, university and email integrity."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        email = cleaned_data.get("email")
        university = cleaned_data.get("university")

        # Validate start_date and end_date
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before start date.")
            if end_date < now().date():
                raise forms.ValidationError("End date must be in the future.")
        
        #Validate email format
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email format. Please enter your univeristy email.")

        #Validate that email matches univeristy
        if university and email:
            domain = "@" + email.split("@")[-1]
            if domain.lower() != university.domain.lower():
                raise forms.ValidationError(f"Email must end with '{domain}'.")
            
        return cleaned_data
    
    def save(self, commit=True):
        """Create a new user."""
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            start_date=self.cleaned_data.get('start_date'),
            end_date=self.cleaned_data.get('end_date'),
            password=self.cleaned_data.get('new_password'),
            user_type="student",
        )

        return user
