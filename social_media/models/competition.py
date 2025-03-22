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
    is_point_based = models.BooleanField(default=False)
    is_finalized = models.BooleanField(
        default=False,
        help_text="If True, no new participants can join or be modified."
    )

    def __str__(self):
        return f"{self.society.name}: {self.name}"

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
    """Model representing a match between either two users."""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="matches")
    round_number = models.PositiveIntegerField(default=1)

    participant1 = models.ForeignKey(
        CompetitionParticipant,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="p1_matches"
    )
    participant2 = models.ForeignKey(
        CompetitionParticipant,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="p2_matches"
    )

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

    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Match #{self.pk} in {self.competition.name}"

   
    def get_opponents(self):
        """Return a tuple of the two participants."""
        return (self.participant1, self.participant2)

    def finalize_result(self, score1=None, score2=None, winner_part=None):
        """Allow admin to set final scores/winners."""
        if score1 is not None:
            self.score_p1 = score1
        if score2 is not None:
            self.score_p2 = score2
        if winner_part:
            self.winner_participant = winner_part

        self.is_finished = True
        self.save()
