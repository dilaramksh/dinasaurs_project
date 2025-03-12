from django.db import models
from django.conf import settings 
from django import forms
from django.core.exceptions import ValidationError
from social_media.models.society import User, Society

class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    