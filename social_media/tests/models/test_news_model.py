from django.test import TestCase
from social_media.models import Category, News, Society, User
from django.core.exceptions import ValidationError
from django.test import TestCase

class NewsModelTestCase(TestCase):
    """Unit tests for the News Model"""

    fixtures = ['social_media/tests/fixtures/default_user.json']

    def setUp(self):
        self.category = Category.objects.create(name="cultural")
        self.society = Society.objects.create(
            name="A Soc",
            society_email="asoc@test.ac.uk",
            founder = User.objects.get(email="john.doe@test.ac.uk"),
            description="A desc.",
            category=self.category,
            paid_membership=True,
            price=10.0,
            colour1="#FFF0FF",
            colour2="#000022",
            termination_reason="operational",
            status="pending",
        )
        self.valid_description = "The description is here!"
        self.long_description = "a" * 1001 

    def test_create_valid_news(self):
        """Test creating a valid news item."""
        news = News(society=self.society, description=self.valid_description)
        news.full_clean()
        news.save()
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(news.likes, 0)
        
    def test_description_required(self):
        """Test an empty description raises ValidationError."""
        news = News(society=self.society, description="")
        with self.assertRaises(ValidationError):
            news.full_clean()

    def test_description_max_length(self):
        """Test exceeding 1000 chars raises ValidationError."""
        news = News(society=self.society, description=self.long_description)
        with self.assertRaises(ValidationError):
            news.full_clean()
