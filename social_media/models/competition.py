from django.db import models
from django.utils import timezone

class Competition(models.Model):
    society = models.ForeignKey('social_media.Society', on_delete=models.CASCADE, related_name="competitions")
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)  # whether competition is ongoing

    def __str__(self):
        return f"{self.society.name}: {self.name}"

class CompetitionParticipant(models.Model):
    user = models.ForeignKey('social_media.User',
                            on_delete=models.CASCADE,
                            limit_choices_to={'user_type': 'student'} 
                            )
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="participants")
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "competition")

    def __str__(self):
        return f"{self.user.username} in {self.competition.name}"


class Match(models.Model):
    """A single match within a competition."""
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="matches")
    participant1 = models.ForeignKey(CompetitionParticipant, on_delete=models.SET_NULL, null=True)
    participant2 = models.ForeignKey(CompetitionParticipant, on_delete=models.SET_NULL, null=True)
    scheduled_time = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(CompetitionParticipant, on_delete=models.SET_NULL, null=True, blank=True, related_name="matches_won")
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"Match #{self.pk} in {self.competition.name}"

    def get_opponents(self):
        """Return a tuple of the two participants."""
        return (self.participant1, self.participant2)



class Ranking(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="rankings")
    user = models.ForeignKey('social_media.User', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(blank=True, null=True)
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ("competition", "user")

    def __str__(self):
        return f"{self.user.username} rank {self.rank or '?'} in {self.competition.name}"

