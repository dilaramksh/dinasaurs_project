from django.core.validators import RegexValidator
from django.db import models
from .society import Society

class SocietyRole(models.Model):
    """Model used for roles allocated to members of a society"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE) 
    role_name = models.CharField(max_length=50, blank=False)