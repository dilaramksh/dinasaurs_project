"""Unit tests of the sign up form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from social_media.forms import SignUpForm
from social_media.models import University
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import now, timedelta
from django.core.validators import ValidationError

class SignUpFormTestCase(TestCase):
    """Unit tests of the sign up form."""

    def setUp(self):
        self.university = University.objects.create(name="Test University", domain="test.ac.uk", status="approved")

        self.form_input = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': '@janedoe',
            'email': 'janedoe@test.ac.uk',
            'university': self.university.id,
            'start_date': '2022-09-01',
            'end_date': '2025-06-30',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'profile_picture' : SimpleUploadedFile("profile.jpg", b"profile_picture_content", content_type="image/jpeg")

        }

    def test_valid_form(self):
        """Test that form is valid."""
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_required_fields(self):
        """Test thatf form has all required fields."""
        form = SignUpForm()
        expected_fields = {"first_name", "last_name", "username", "university", "email", "start_date", "end_date", "profile_picture", "new_password", "password_confirmation"}
        self.assertEqual(set(form.fields.keys()), expected_fields)

    def test_valid_form_submission(self):
        """Test that form submits correctly."""
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_missing_email_field(self):
        """Test that missing email triggers ValidationError."""
        form = SignUpForm(data=self.form_input)
        form.cleaned_data = self.form_input 
        form.cleaned_data['email'] = ""      

        with self.assertRaises(ValidationError) as cm:
            form.clean_email()
        self.assertEqual(str(cm.exception), "['Email is required.']")

    def test_invalid_email_format(self):
        """Test invalid email format."""
        form = SignUpForm(data=self.form_input)
        form.cleaned_data = self.form_input
        form.cleaned_data['email'] = "invalid-email"

        with self.assertRaises(ValidationError) as cm:
            form.clean_email()
        self.assertEqual(
            str(cm.exception),
            "['Invalid email format. Please enter your university email.']"
        )

    def test_email_must_match_university_domain(self):
        """Test that email domain matches that of selected university."""
        self.form_input["email"] = "janedoe@gmail.com"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
    
    def test_missing_university_field(self):
        """Test that univeristy is selected."""
        self.form_input.pop("university") 
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, "university", "Please select a university.")


    def test_start_date_must_be_before_end_date(self):
        """Test that selected start date is before end date."""
        self.form_input["start_date"] = (now() + timedelta(days=10)).date()
        self.form_input["end_date"] = now().date()
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_end_date_must_be_in_future(self):
        """Test that selected end date is after current date."""
        self.form_input["end_date"] = (now() - timedelta(days=10)).date()
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("end_date", form.errors)

    def test_password_requires_uppercase(self):
        """Test that password contains uppercase letter."""
        self.form_input["new_password"] = "password123"
        self.form_input["password_confirmation"] = "password123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_requires_lowercase(self):
        """Test that password contains lowecase letter."""
        self.form_input["new_password"] = "PASSWORD123"
        self.form_input["password_confirmation"] = "PASSWORD123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_requires_number(self):
        """Test that password contains number letter."""
        self.form_input["new_password"] = "PasswordABC"
        self.form_input["password_confirmation"] = "PasswordABC"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_passwords_must_match(self):
        """Test that password input and confirmation are identical. """
        self.form_input["password_confirmation"] = "WrongPassword123"
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn("password_confirmation", form.errors)

    def test_form_save_creates_user(self):
        """Test that new users are saved correctly in database"""
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, self.form_input["username"])
        self.assertEqual(user.email, self.form_input["email"])
        self.assertEqual(user.university.id, self.form_input["university"])
        self.assertTrue(check_password("Password123", user.password))


