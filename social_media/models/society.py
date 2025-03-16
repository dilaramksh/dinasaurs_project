
from django.core.validators import EmailValidator, MaxValueValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
from .user import User
from .category import Category

class Society(models.Model):
    """Model used for information on societies"""
    name = models.CharField(max_length=50, blank=False)
    founder = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'}) 
    society_email = models.EmailField(unique=True, blank=False, validators=[EmailValidator()])
    description = models.CharField(max_length=2000, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    paid_membership = models.BooleanField(default=False, blank=False) #all memberships are free by default
    price = models.FloatField(default=0.0, validators=[MaxValueValidator(50.0)])
    colour1 = models.CharField(
        max_length=7,
        default= "#FFD700",
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message="Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF",
            )
        ]
    )
    colour2 = models.CharField(
        max_length=7,
        default="#FFF2CC", 
        validators=[
            RegexValidator(
                regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$',
                message="Enter a valid hexadecimal colour code, e.g., #FFFFFF or #FFF",
            )
        ]
    )
    #logo = models.ImageField(upload_to='news_images/', blank=False) #stores image of the logo
    termination_reason = models.CharField(max_length=50, choices=[('operational', 'Operational reasons'), ('low_interest', 'Low Interest'), ('financial', 'Financial reasons'), ('other', 'Other reason') ])
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("blocked", "Blocked")], default="pending")
    
    def clean(self):
        super().clean()  # Call any default validation logic

        if not self.paid_membership:
            if self.price != 0:
                raise ValidationError("Price must be zero for a free membership.")
        else:
            if self.price <= 0:
                raise ValidationError("Price must be greater than zero for a paid membership.")
    
    def approve(self):
        """Approve the society."""
        self.status = "approved"
        self.save()

    def block(self):
        """Block the society."""
        self.status = "blocked"
        self.save()

    def __str__(self):
        return self.name