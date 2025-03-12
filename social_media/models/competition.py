from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Competition(models.Model):
    """Model of a competition within a society."""
    society = models.ForeignKey('social_media.Society', on_delete=models.CASCADE, related_name="competitions")
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_ongoing = models.BooleanField(default=True)
    is_team_based = models.BooleanField(default=False)
    is_finalized = models.BooleanField(
        default=False,
        help_text="If True, no new participants or teams can join or be modified."
    )

    def __str__(self):
        return f"{self.society.name}: {self.name}"


class Team(models.Model):
    """Model used for a team in a team-based competition."""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=100)
    is_eliminated = models.BooleanField(default=False)
    # optional fields: allow society admin to choose whether competition is point/rank based
    points = models.FloatField(default=0.0, blank=True)
    rank = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Team in {self.competition.name})"


class TeamMembership(models.Model):
    """Model used to record users in a team for a competition."""
    user = models.ForeignKey('social_media.User', on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    date_joined = models.DateTimeField(auto_now_add=True)
   
    class Meta:
        # A user can only be in one team in the same competition
        constraints = [
            models.UniqueConstraint(
                fields=["user", "team"], name="unique_user_per_team"
            )
        ]

    def clean(self):
        # Ensure user not in more than one teams for the same competition
        competition_id = self.team.competition_id
        existing = TeamMembership.objects.filter(
            user=self.user,
            team__competition_id=competition_id
        ).exclude(pk=self.pk).exists()
        if existing:
            raise ValidationError("User is already in another team for this competition!")

    def __str__(self):
        return f"{self.user.username} -> {self.team.name}"


class CompetitionParticipant(models.Model):
    """Model used for recording individual participants in a competition."""
    user = models.ForeignKey('social_media.User',
                            on_delete=models.CASCADE,
                            limit_choices_to={'user_type': 'student'} 
                            )
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="participants")
    date_joined = models.DateTimeField(auto_now_add=True)
    is_eliminated = models.BooleanField(default=False)
    points = models.FloatField(default=0.0, blank=True)
    rank = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        unique_together = ("user", "competition")

    def __str__(self):
        return f"{self.user.username} in {self.competition.name}"


class Match(models.Model):
    """Model representing a match between either two users/two teams."""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="matches")
    round_number = models.PositiveIntegerField(default=1)

    # For individual competitions
    participant1 = models.ForeignKey(
        CompetitionParticipant,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    participant2 = models.ForeignKey(
        CompetitionParticipant,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    # For team-based competitions
    team1 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    team2 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    scheduled_time = models.DateTimeField(blank=True, null=True)

    # Admin can record numeric scores or pick a winner
    score_p1 = models.FloatField(blank=True, null=True)
    score_p2 = models.FloatField(blank=True, null=True)

    winner_participant = models.ForeignKey(
        CompetitionParticipant,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="matches_won"
    )
    winner_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="matches_won")

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Match #{self.pk} in {self.competition.name}"

    def clean(self):
        if self.competition.is_team_based:
            # If team1/team2 is set, participant1/2 must not be set
            if not (self.team1 and self.team2) or (self.participant1 or self.participant2):
                raise ValidationError("Team-based match must have team1/team2 set, not participants!")
        else:
            # If participant1/2 is set, team1/team2 must not be set
            if not (self.participant1 and self.participant2) or (self.team1 or self.team2):
                raise ValidationError("Individual match must have participant1/participant2, not teams.")

    def get_opponents(self):
        """Return a tuple of the two participants."""
        return (self.participant1, self.participant2)

    def finalize_result(self, score1=None, score2=None, winner_part=None, winner_t=None):
        """Allow admin to set final scores/winners."""
        if score1 is not None:
            self.score_p1 = score1
        if score2 is not None:
            self.score_p2 = score2
        if winner_part:
            self.winner_participant = winner_part
        if winner_t:
            self.winner_team = winner_t

        self.is_finished = True
        self.save()
