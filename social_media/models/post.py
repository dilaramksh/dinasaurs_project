from django.db import models
from django.conf import settings 
from django import forms
from django.core.exceptions import ValidationError
from social_media.models.society import User, Society


class Post(models.Model):
    """
    Model used for creating posts within a society.

    This model represents a post created by a user within a society. It includes details such as
    the post's title, content, creation date, author, associated society, and an optional picture.

    Attributes:
        title (CharField): The title of the post.
        content (TextField): The content of the post.
        created_at (DateTimeField): The date and time when the post was created.
        author (ForeignKey): A reference to the user who created the post.
        society (ForeignKey): A reference to the society where the post was created.
        picture (ImageField): An optional field for uploading a picture related to the post.
    """
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="posts")
    picture = models.ImageField(upload_to="post_pictures/", blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    