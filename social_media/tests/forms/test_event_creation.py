from django.test import TestCase
from django.core.exceptions import ValidationError
from social_media.forms import EventCreationForm
from social_media.models import Event, Society, User, University, Category
from datetime import date, timedelta

class EventCreationFormTest(TestCase):
    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        """
        self.university = University.objects.create(
            name= "Test University",
            domain = "test.ac.uk",
            status= "accepted",
            logo="university_logos/default.png",
        )

        self.user = User.objects.create_user(
            first_name = "test",
            last_name = "testington",
            username='@testuser', 
            email='test@test.ac.uk', 
            user_type= 'student',
            university=self.university,
            start_date= date(2023,1,1),
            end_date = date(2027,1,1),
            profile_picture = "profile_picture/default.jpg",
            password='Password123',
        )

        self.category = Category.objects.create(
            name='cultural',
        )
        
        self.society = Society.objects.create(
            name = "Test Society",
            founder = self.user,
            society_email = "testsociety@test.ac.uk",
            description = "Test description",
            category = self.category,
            paid_membership = False,
            price = 0.0,
            colour1 = "#FFD700",
            colour2 = "#FFF2CC",
            logo = "society_logos/default.jpg",
            termination_reason = 'Other reason',
            status = "approved",
        )

        self.valid_data = {
            "name": "Test Event",
            "description": "Test event Description", 
            "date": date(2025,7,27), 
            "location": "Test location", 
        }

    def test_form_valid_with_all_required_fields(self):
        """
        Test that the form is valid when all required fields are provided correctly.
        """
        
        form = EventCreationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_past_date(self):
        """
        Test that the form is invalid when the event date is in the past.
        """
        form_data = {
            "name": "Test Event",
            "description": "Test event Description", 
            "date": date.today() - timedelta(days=300), 
            "location": "Test location",
        }
        
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_invalid_with_missing_fields(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form_data = {
            "name": "Test Event",
        }
        
        form = EventCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors) > 1)

