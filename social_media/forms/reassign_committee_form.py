from django import forms
#from django.contrib.auth.models import User
from social_media.models import Membership, User

class CommitteeReassignForm(forms.Form):
    committee_member = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="-- Select Member --")

    def __init__(self, *args, **kwargs):
        self.committee = kwargs.pop('committee')
        super().__init__(*args, **kwargs)
        self.fields['committee_member'].queryset = User.objects.exclude(id__in=[member.id for member in self.committee.members.all()])
