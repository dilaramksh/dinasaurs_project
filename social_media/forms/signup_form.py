from django import forms
from django.core.validators import EmailValidator, ValidationError
from social_media.models import User, University
from social_media.mixins import NewPasswordMixin
from django.utils.timezone import now

class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    university = forms.ModelChoiceField(
        queryset=University.objects.all(), 
        empty_label="Select a University",
        label="University"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'university', 'start_date', 'end_date']
        widgets = {
            #'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            #'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            #'username': forms.TextInput(attrs={'class': 'form-control'}),
            #'email': forms.EmailInput(attrs={'class': 'form-control'}),
            #'university': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    
    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        
        if end_date <= start_date:
            raise ValidationError('End date must be after the start date.')
        
        if end_date <= now().date():
            raise ValidationError('End date must be in the future.')
        
        return end_date
    
    """
    def clean(self):
        print(f"Field errors before clean(): {self.errors}")
        
        cleaned_data = super().clean()

        print("DEBUG: cleaned_data - ", cleaned_data)

        if not cleaned_data:
            raise forms.ValidationError("Form data could not be cleaned.")  # 
        
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        email = cleaned_data.get("email")
        university = cleaned_data.get("university")

        # Validate start_date and end_date
        if start_date and end_date:
            if end_date < start_date:
                self.add_error("end_date", "End date cannot be before start date.")  
            if end_date < now().date():
                self.add_error("end_date", "End date must be in the future.") 
        
        #Validate email format
        if email:
            validator = EmailValidator()
            try:
                validator(email)
            except ValidationError:
                self.add_error("email", "Invalid email format. Please enter your university email.")  

        
        #Validate that email matches univeristy
        if university and email:
            email_domain = email.split("@")[-1]
            if email_domain.lower() != university.domain.lower():
                self.add_error("email", f"Email must end with '{university.domain}'.") 
            
        return cleaned_data
    """

    def save(self):
        """Create a new user."""
        print("DEBUG: Data before saving -", self.cleaned_data)

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
        )
    
        return user
 