from django.core.validators import RegexValidator
from django.db import models
from .user import User
from .society_role import SocietyRole
from .society import Society
from django.core.exceptions import ValidationError


class Membership(models.Model):
    """Model used for recording members in a society and their roles within the society"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE) 
    society_role = models.ForeignKey(SocietyRole, on_delete=models.CASCADE)

    class Meta:
        """Ensure a user can only join a society once, regardless of role"""
        constraints = [
            models.UniqueConstraint(fields=["user", "society"], name="unique_user_in_society")
        ]

    def clean(self):
        """Prevent memberships in non-approved societies"""
        if self.society.status != "approved":
            raise ValidationError("Cannot create membership for a non-approved society.")

    def is_committee_member(self):
        """Returns True if the membership is a committee role."""
        return self.society_role.is_committee_role()

    def __str__(self):
        return f"{self.user.username} - {self.society.name} ({self.society_role.role_name})"
