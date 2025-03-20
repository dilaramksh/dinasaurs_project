from django import forms
#from django.contrib.auth.models import User
from social_media.models import Membership, User

class CommitteeReassignForm(forms.Form):
    """
    Form for reassigning committee members within a society.

    This form allows users to select a new committee member from a list of users
    who are not already part of the committee.

    Attributes:
        committee_member (ModelChoiceField): A dropdown field for selecting a new committee member.
    """

    committee_member = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="-- Select Member --")

    def __init__(self, *args, **kwargs):
        self.committee = kwargs.pop('committee')
        super().__init__(*args, **kwargs)
        self.fields['committee_member'].queryset = User.objects.exclude(id__in=[member.id for member in self.committee.members.all()])
