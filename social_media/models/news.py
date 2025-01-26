from django.db import models

from .society import Society

class News(models.Model):
    """Model used for news in the society"""

    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=False)
    # image = models.ImageField(upload_to='news_images/', blank=False)
    likes = models.IntegerField(default=0)