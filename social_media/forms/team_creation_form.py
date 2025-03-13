from django import forms
from social_media.models import CompetitionParticipants

class CreateTeamForm(forms.Form):
    team_name = forms.CharField(label="Team Name", max_length=100)

    def __init__(self, *args, **kwargs):
        self.competition = kwargs.pop("competition", None)
        super().__init__(*args, **kwargs)

        available_participants = CompetitionParticipants.objects.filter(
            competition=self.competition
        ).exclude(
            user__teammembership__team__competition=self.competition
        )

        self.fields["participants"] = forms.ModelMultipleChoiceField(
            queryset=available_participants,
            required=False,
            widget=forms.CheckboxSelectMultiple,
            label="Select Participants to Assign"
        )
