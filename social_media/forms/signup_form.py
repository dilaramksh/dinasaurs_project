from django import forms
from django.core.validators import EmailValidator, ValidationError
from social_media.models import User, University
from social_media.mixins import NewPasswordMixin
from django.utils.timezone import now

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    profile_picture = forms.ImageField(required=False)

    university = forms.ModelChoiceField(
        queryset=University.objects.filter(status='approved'),
        empty_label="Select a University",
        label="University",
        error_messages={'required': "Please select a university."}
    ) 

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'university', 'email', 'start_date', 'end_date', 'profile_picture']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_end_date(self):
        """Ensure the end date is after the start date."""

        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        
        if end_date <= start_date:
            raise ValidationError('End date must be after the start date.')
        
        if end_date <= now().date():
            raise ValidationError('End date must be in the future.')
        
        return end_date
    
    def clean_email(self):
        """Ensure the email is valid and belongs to the selected university."""

        email = self.cleaned_data.get('email')
        university = self.cleaned_data.get('university')

        if not email:
            raise ValidationError("Email is required.")
        
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            raise ValidationError("Invalid email format. Please enter your university email.")
        
        if not university:
            raise ValidationError("Please select a university.")

        if university and email:
            email_domain = email.split("@")[-1]
            if email_domain.lower() != university.domain.lower():
                raise ValidationError(f"Email must end with '{university.domain}'.") 

        return email


    def save(self):
        """Create a new user."""
    
        university_id = self.cleaned_data.get('university').id
        university = University.objects.get(id=university_id) 

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            university = university, 
            start_date=self.cleaned_data.get('start_date'),
            end_date=self.cleaned_data.get('end_date'),
            password=self.cleaned_data.get('new_password'),
            user_type="student",
            profile_picture = self.cleaned_data["profile_picture"]
        )

        return user

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        return username.strip()

 