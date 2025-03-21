from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to="profile_pictures/")
    uploaded_at = models.DateTimeField(auto_now_add=True)