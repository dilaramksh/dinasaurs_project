from django.core.validators import RegexValidator
from django.db import models
from .society import Society

class SocietyRole(models.Model):
    """Model used for roles allocated to members of a society"""
    society = models.ForeignKey(Society, on_delete=models.CASCADE) 
    role_name = models.CharField(max_length=50, blank=False)

    class Meta:
        """Each society has unique role names."""
        constraints = [
            models.UniqueConstraint(fields=["society", "role_name"], name="unique_society_role")
        ]
       

    def __str__(self):
        return f"{self.society.name} - {self.role_name}"

    def is_committee_role(self):
        """Determine if the role is a committee role."""
        #Change to standard member in seeder?
        return self.role_name.lower() not in ["member", "standard member"]