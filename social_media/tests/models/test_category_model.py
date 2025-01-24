from django.test import TestCase
from django.core.exceptions import ValidationError
from social_media.models import Category

class CategoryModelTest(TestCase):
    """Unit tests for the Category Model"""

    def setUp(self):
        self.valid_name = "cultural"
        self.invalid_name = "invalid_category"

    def test_create_valid_category(self):
        """Test that a category with a valid name can be created."""
        category = Category(name=self.valid_name)
        category.full_clean()  # Should not raise ValidationError
        category.save()
        self.assertEqual(Category.objects.count(), 1)

    def test_invalid_category_name(self):
        """Test that a category with an invalid name raises a validation error."""
        category = Category(name=self.invalid_name)
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_empty_category_name(self):
        """Test that an empty name raises a validation error."""
        category = Category(name="")
        with self.assertRaises(ValidationError):
            category.full_clean()

    def test_name_choices_validation(self):
        """Test that only valid choices for the name field are accepted."""
        valid_choices = [
            'cultural', 'academic_career', 'faith', 'political', 'sports', 'volunteering', 'other'
        ]
        for choice in valid_choices:
            category = Category(name=choice)
            category.full_clean()  # Should not raise ValidationError
            category.save()

        self.assertEqual(Category.objects.count(), len(valid_choices))

    def test_duplicate_category(self):
        """Test that duplicate categories with the same name can exist (if not unique)."""
        category1 = Category(name=self.valid_name)
        category2 = Category(name=self.valid_name)
        category1.full_clean()
        category1.save()
        category2.full_clean()
        category2.save()
        self.assertEqual(Category.objects.count(), 2)
