from django import forms
from social_media.models.competition import Competition

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ["name", "start_date", "end_date","is_point_based"]
