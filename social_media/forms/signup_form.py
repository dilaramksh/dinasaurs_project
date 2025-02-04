from django import forms
from social_media.models import User
from social_media.mixins import NewPasswordMixin
from django.utils.timezone import now

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'university', 'start_date', 'end_date']

    def clean(self):
        """Ensure date integrity."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Validate start_date and end_date
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date cannot be before start date.")
            if end_date < now().date():
                raise forms.ValidationError("End date must be in the future.")

        return cleaned_data
    
    def save(self):
        """Create a new user."""
        super().save(commit=False)  
        user = User.objects.create_user(
            username=self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
            user_type="student", #Default user type
        )

        return user