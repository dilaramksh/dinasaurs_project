from django.test import TestCase
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from social_media.models import Society, Category
from social_media.models.colour_history import SocietyColorHistory
from social_media.models.university import University

User = get_user_model()

class SocietyColorHistoryTest(TestCase):
    """Test cases for the SocietyColorHistory model."""

    def setUp(self):
        """Set up test data before each test."""
        self.university = University.objects.create(name="Test University")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            user_type="student",
            university=self.university,
            start_date=now().date(),  # Provide a value for the start_date field
            end_date=now().date()  # Provide a value for the end_date field
        )
        self.category = Category.objects.create(name="Test Category")
        self.society = Society.objects.create(
            name="Test Society",
            founder=self.user,
            society_email="test@society.com",
            description="A test society",
            category=self.category,
            paid_membership=False,
            price=0.0,
            colour1="#FFD700",
            colour2="#FFF2CC",
            termination_reason="operational",
            status="pending"
        )
        self.color_history = SocietyColorHistory.objects.create(
            society=self.society,
            previous_colour1="#ff0000",
            previous_colour2="#00ff00",
            updated_at=now()
        )

    def test_color_history_creation(self):
        """Test if a SocietyColorHistory instance is correctly created."""
        self.assertEqual(self.color_history.society, self.society)
        self.assertEqual(self.color_history.previous_colour1, "#ff0000")
        self.assertEqual(self.color_history.previous_colour2, "#00ff00")
        self.assertIsNotNone(self.color_history.updated_at)

    def test_color_history_str_representation(self):
        """Test the string representation of a SocietyColorHistory instance."""
        expected_str = f"{self.society.name} Colors: {self.color_history.previous_colour1}, {self.color_history.previous_colour2} at {self.color_history.updated_at}"
        self.assertEqual(str(self.color_history), expected_str)

    def test_color_history_retrieval(self):
        """Test if the SocietyColorHistory instance can be retrieved from the database."""
        retrieved_history = SocietyColorHistory.objects.get(id=self.color_history.id)
        self.assertEqual(retrieved_history, self.color_history)

    def test_color_history_deletion(self):
        """Test if a SocietyColorHistory instance is successfully deleted."""
        history_id = self.color_history.id
        self.color_history.delete()
        with self.assertRaises(SocietyColorHistory.DoesNotExist):
            SocietyColorHistory.objects.get(id=history_id)