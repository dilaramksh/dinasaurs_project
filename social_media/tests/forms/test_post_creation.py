from django.test import TestCase
from social_media.forms import PostForm

class PostFormTest(TestCase):
    def test_valid_form(self):
        """Test if PostForm is valid with correct data."""
        form_data = {
            "title": "Valid Post Title",
            "content": "This is a valid post content."
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        """Test if PostForm is invalid when title is missing."""
        form_data = {
            "title": "",
            "content": "This post has no title."
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_missing_content(self):
        """Test if PostForm is invalid when content is missing."""
        form_data = {
            "title": "Title exists",
            "content": ""
        }
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)


    def test_title_length(self):
        """Test if PostForm handles long titles."""
        long_title = "A" * 300 
        form_data = {
            "title": long_title,
            "content": "This is valid content."
        }
        form = PostForm(data=form_data)

        self.assertFalse(form.is_valid())  
        self.assertIn("title", form.errors)