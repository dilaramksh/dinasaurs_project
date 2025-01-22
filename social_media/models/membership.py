from django.core.validators import RegexValidator
from django.db import models
from .user import User
from .society_role import SocietyRole

class Membership(models.Model):
    """Model used for recording members in a society and their roles within the society"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role =  models.ForeignKey(SocietyRole, on_delete=models.CASCADE)
   