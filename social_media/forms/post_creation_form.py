from django import forms
from social_media.models.post import Post

class PostForm(forms.ModelForm):

    picture = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ["title", "content", "picture"]