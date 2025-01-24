
from django.core.validators import EmailValidator, MaxValueValidator, RegexValidator
from django.db import models

from .user import User
from .category import Category

class Society(models.Model):
    """Model used for information on societies"""
    name = models.CharField(max_length=50, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 
    society_email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()])
    description = models.CharField(max_length=2000, blank=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    paid_membership = models.BooleanField(default=False, blank=False) #all memberships are free by default
    price = models.FloatField(validators=[MaxValueValidator(50.0)])
    colour1 = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message="Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF",
            )
        ]
    )
    colour2 = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message="Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF",
            )
        ]
    )
    #logo = models.ImageField(upload_to='news_images/', blank=False) #stores image of the logo
    termination_reason = models.CharField(max_length=50, choices=[('operational', 'Operational reasons'), ('low_interest', 'Low Interest'), ('financial', 'Financial reasons'), ('other', 'Other reason') ])
    is_active = models.BooleanField(blank=False) #this allows the university admins to approve or reject, as well as terminate the society if need be
