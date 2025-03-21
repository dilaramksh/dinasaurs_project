from django import forms
from social_media.models.post import Post

class PostForm(forms.ModelForm):
    """
    Form for creating and editing posts within a society.

    This form allows users to input details about the post such as title, content,
    and an optional picture.

    Attributes:
        picture (ImageField): An optional field for uploading a post picture.
    """

    picture = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "picture"]
        help_texts = {
            'title': 'Enter the title of the post.',
            'content': 'Enter the content of the post.',
            'picture': 'Upload an optional picture for the post.',
        }