from django.test import TestCase
from django.utils.timezone import now
from social_media.models.society import Society
from social_media.models.colour_history import SocietyColorHistory

class SocietyColorHistoryTest(TestCase):

    def setUp(self):
        """Set up a test Society instance."""
        self.society = Society.objects.create(
            name="Tech Society",
            society_email="tech@example.com",
            description="A society for tech enthusiasts",
            category="Technology",
            price=10,
            colour1="#FF5733",
            colour2="#33FF57"
        )

    def test_create_color_history_entry(self):
        """Test if a SocietyColorHistory entry can be created successfully."""
        color_history = SocietyColorHistory.objects.create(
            society=self.society,
            previous_colour1="#123456",
            previous_colour2="#654321"
        )

        self.assertEqual(color_history.society, self.society)
        self.assertEqual(color_history.previous_colour1, "#123456")
        self.assertEqual(color_history.previous_colour2, "#654321")

    def test_updated_at_auto_timestamp(self):
        """Test if the updated_at field is automatically set."""
        color_history = SocietyColorHistory.objects.create(
            society=self.society,
            previous_colour1="#ABCDEF",
            previous_colour2="#FEDCBA"
        )

        self.assertIsNotNone(color_history.updated_at)
        self.assertAlmostEqual(color_history.updated_at, now(), delta=2)

    def test_foreign_key_relationship(self):
        """Test if deleting a Society also deletes its color history (CASCADE)."""
        color_history = SocietyColorHistory.objects.create(
            society=self.society,
            previous_colour1="#000000",
            previous_colour2="#FFFFFF"
        )

        self.assertEqual(SocietyColorHistory.objects.count(), 1)

        self.society.delete()

        self.assertEqual(SocietyColorHistory.objects.count(), 0)

    def test_invalid_hex_color_length(self):
        """Test if invalid hex color length raises an error."""
        with self.assertRaises(ValueError):
            SocietyColorHistory.objects.create(
                society=self.society,
                previous_colour1="12345",
                previous_colour2="INVALID"
            )
