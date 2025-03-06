from django import forms
from social_media.models.profile_pictures import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ["image"]